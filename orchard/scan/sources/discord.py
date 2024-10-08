import logging

import httpx
import urllib.parse

from orchard.scan.sources.interface import RDLevelScraper
from orchard.utils.client import Client
from orchard.utils.constants import DISCORD_API_URL, USER_AGENT

BATCH_SIZE = 100

logger = logging.getLogger(__name__)


def get_iid_info(iid):
    message_id, attachment_id = [int(s) for s in iid.split("|")]
    return message_id, attachment_id


class DiscordScraper(RDLevelScraper):
    """
    Scrape a discord server for rdzips. It works on a specific channel.
    bot_token : token for the bot user that does the scraping.
    channel_id: id of the channel. not sure how this will work with forum channels?
    start_timestamp: when to start scanning from. this is a discord snowflake
    """

    def __init__(self, bot_token, channel_id, after):
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.after = after
        self.iid_cache = {}  # cache of iids to discord Message objects.
        # self.iid_url_map = {}
        # get our id.
        resp = httpx.get(
            f"{DISCORD_API_URL}/users/@me",
            headers={
                "user-agent": USER_AGENT,
                "Authorization": f"Bot {self.bot_token}",
            },
        )
        self.bot_id = resp.json()["id"]

    async def download_iid(self, iid):
        url = await self.get_url(iid)
        return httpx.get(url).content

    async def get_message(self, iid):
        "Get the discord Message object relating to an iid. Has an internal cache."
        if iid in self.iid_cache:
            return self.iid_cache[iid]
        else:
            # we need to do an API request to get the message.
            message_id, _ = get_iid_info(iid)
            async with Client() as client:
                headers = {
                    "user-agent": USER_AGENT,
                    "Authorization": f"Bot {self.bot_token}",
                }
                resp = await client.get(
                    f"{DISCORD_API_URL}/channels/{self.channel_id}/messages/{message_id}",
                    headers=headers,
                )
                message = resp.json()
                # put it in the cache before we keep going.
                self.iid_cache[iid] = message
                return message

    async def get_url(self, iid):
        _, attachment_id = get_iid_info(iid)
        message = await self.get_message(iid)

        attachment = next(
            a for a in message["attachments"] if int(a["id"]) == attachment_id
        )
        return attachment["url"]

    async def get_metadata(self, iid):
        message = await self.get_message(iid)

        return {"user_id": message["author"]["id"], "timestamp": message["timestamp"]}

    async def check_reaction(self, post, emoji):
        if not "reactions" in post:
            return False

        if emoji not in [react["emoji"]["name"] for react in post["reactions"]]:
            return False

        async with Client() as client:
            react_params = {"limit": 100}
            reactors = await client.get(
                f"{DISCORD_API_URL}/channels/{self.channel_id}/messages/{post['id']}/reactions/{urllib.parse.quote(emoji)}",
                headers={
                    "user-agent": USER_AGENT,
                    "Authorization": f"Bot {self.bot_token}",
                },
                params=react_params,
            )

            for reactor in reactors.json():
                if (
                    reactor["id"] == post["author"]["id"]
                    or reactor["id"] == self.bot_id
                ):
                    return True

            return False

    async def get_iids(self):
        iids = []
        current_after = self.after
        async with Client() as client:
            while True:
                params = {"after": current_after, "limit": BATCH_SIZE}
                headers = {
                    "user-agent": USER_AGENT,
                    "Authorization": f"Bot {self.bot_token}",
                }
                logger.info(
                    f"Scanning for {BATCH_SIZE} levels after snowflake {current_after}"
                )
                resp = await client.get(
                    f"{DISCORD_API_URL}/channels/{self.channel_id}/messages",
                    headers=headers,
                    params=params,
                )
                posts = resp.json()
                if len(posts) == 0:
                    break

                # scan each to see if it has levels (attachments ending with .rdzip)
                for post in posts:
                    # if the post is later than our current, use it for the next _after_ parameter.
                    # note: snowflakes are sequential and have an encoded timestamp.
                    # note2: even if the post has a :no-entry-sign:, we still need to think about it for pagination.
                    if int(post["id"]) > current_after:
                        current_after = int(post["id"])

                    # check the post does not have a :no-entry-sign: by the OP.
                    remove_attachments = await self.check_reaction(post, "🚫")

                    # a message can only have a maximum of 10 attachments, so we use number reactions
                    number_reactions = [
                        "1️⃣",
                        "2️⃣",
                        "3️⃣",
                        "4️⃣",
                        "5️⃣",
                        "6️⃣",
                        "7️⃣",
                        "8️⃣",
                        "9️⃣",
                        "🔟",
                    ]

                    # check all attachments and corresponding number reactions. if no number reaction is found, then we ignore every attachment
                    ignore_all_attachments = True
                    attachment_numbers = []
                    relative_position = 0
                    for i, attachment in enumerate(post["attachments"]):
                        if attachment["filename"].endswith(".rdzip"):
                            if remove_attachments and await self.check_reaction(
                                post, number_reactions[relative_position], True
                            ):
                                ignore_all_attachments = False
                                continue
                            attachment_numbers.append(i)
                            relative_position += 1

                    if (not remove_attachments) or (not ignore_all_attachments):
                        for i in attachment_numbers:
                            # the iid is a concatenation of:
                            #  message id, attachment id
                            #  note: the channel id is not required because channels are immutable by source id.
                            #  note2: attachment id is required because it's possible to delete an attachment
                            #         w/o deleting the post.
                            iid = f"{post['id']}|{post['attachments'][i]['id']}"
                            #  cache of message objects for later use, if needed.
                            self.iid_cache[iid] = post
                            iids.append(iid)

                print("", end="")  # <-- for a breakpoint

            return iids

    async def on_index(self, level):
        # react to the post.
        headers = {"user-agent": USER_AGENT, "Authorization": f"Bot {self.bot_token}"}
        message_id, index = get_iid_info(level["source_iid"])
        async with Client() as client:
            await client.put(
                f"{DISCORD_API_URL}/channels/{self.channel_id}/messages/{message_id}/reactions/%E2%9C%85/@me",
                headers=headers,
            )
