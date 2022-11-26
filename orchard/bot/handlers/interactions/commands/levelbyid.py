import httpx

from orchard.bot.lib.comm.interactor import Interactor
from orchard.bot.lib.entities.typesense import ts_get_by_id
from orchard.bot.lib.utils import get_slash_args, grouper
from orchard.bot.lib.comm.message_builder import MessageBuilder as M, Embed


async def levelbyid(body, _):
    async with Interactor(body["token"]) as i:
        [id] = get_slash_args(["id"], body)
        id = id.rstrip()
        try:
            data = await ts_get_by_id(id)
        except httpx.HTTPError:
            await i.edit(
                M().content(f"Could not find a level with id {id}"), "@original"
            )
        else:
            # todo: format this nicely instead of just chucking it all in an embed
            embeds = []
            for items in grouper(20, data.items()):
                embed = Embed()
                for key, value in items:
                    embed = embed.field(key, str(value), True)
                embeds.append(embed)

            message = M()
            for embed in embeds:
                message = message.embed(embed)

            await i.edit(message, "@original")