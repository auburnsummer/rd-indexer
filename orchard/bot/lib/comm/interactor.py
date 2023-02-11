import functools
import logging

from orchard.bot.lib.comm.message_builder import MessageBuilder, start_message
import httpx

from orchard.bot.lib.constants import APPLICATION_ID
from orchard.utils.constants import DISCORD_API_URL

from orchard.bot.lib.comm import pager
from typing import Callable, List, Awaitable

base_url = f"{DISCORD_API_URL}/webhooks/{APPLICATION_ID}"

logger = logging.getLogger(__name__)


def could_raise(func: Callable[[], Awaitable[httpx.Response]]):
    """
    Decorator. Apply to an async function that returns a Response, and it will call raise_for_status first.
    """

    async def inner(*args, **kwargs):
        resp = await func(*args, **kwargs)
        resp.raise_for_status()
        return resp

    return inner


class Interactor:
    """
    A class that contains methods for handling a slash command interaction.
    """

    _token: str
    client: httpx.AsyncClient
    crosscode_uuids: List[pager.PagerUUID]

    def __init__(self, token):
        self._token = token
        self.client = httpx.AsyncClient()
        # list of crosscode uuids which this interactor owns
        self.crosscode_uuids = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        # remove any remaining UUIDS.
        for uuid in self.crosscode_uuids:
            pager.clean(uuid)
        # if there's an exception, edit the message with a default thing.
        if exc_type is not None:
            logger.error("Error", exc_info=True)
            await self.edit(
                start_message()
                .start_embed()
                .title("An error occured!")
                .description(str(exc_value))
                .footer(text=repr(exc_type))
                .done(),
                "@original",
            )
        await self.client.aclose()
        return True  # don't propogate any error

    @could_raise
    async def get(self, id):
        """
        Wrapper around discord API get message (from this webhook)
        """
        return await self.client.get(f"{base_url}/{self._token}/messages/{id}")

    @could_raise
    async def edit(self, mb: MessageBuilder, id):
        """
        Wrapper around discord API edit message.

        https://discord.com/developers/docs/resources/webhook#edit-webhook-message
        """
        return await self.client.patch(
            f"{base_url}/{self._token}/messages/{id}", json=mb.payload()
        )

    @could_raise
    async def post(self, mb: MessageBuilder):
        """
        Wrapper around discord API post message.

        https://discord.com/developers/docs/interactions/receiving-and-responding#create-followup-message
        """
        return await self.client.post(f"{base_url}/{self._token}", json=mb.payload())

    @could_raise
    async def delete(self, id):
        """
        Wrapper around discord API delete message.
        """
        return await self.client.delete(f"{base_url}/{self._token}/messages/{id}")

    def uuid(self):
        """
        Return a new UUID. Adds it to a list for cleanup after.
        """
        new_uuid = pager.new()
        self.crosscode_uuids.append(new_uuid)
        return new_uuid
