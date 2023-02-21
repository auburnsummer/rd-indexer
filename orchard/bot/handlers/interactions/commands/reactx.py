from orchard.bot.lib.comm.message_builder import MessageBuilder
from orchard.bot.lib.slash_commands.slash_router import (
    ApplicationCommandType,
    SlashRoute,
    RouteType,
)
from orchard.bot.lib.comm.interactor import Interactor


async def _reactx(body, _):
    async with Interactor(body["token"]) as i:
        channel_id = body["channel_id"]
        token = body["token"]
        messages = body["data"]["resolved"]["messages"]
        for key, value in messages.items():
            message_id = value["id"]
            await i.react(channel_id, message_id, "🚫")
        await i.edit(MessageBuilder().content("done."), "@original")


reactx = SlashRoute(
    name="reactx",
    description="",
    handler=_reactx,
    default_permission=False,
    defer=RouteType.DEFER_EPHEMERAL,
    type=ApplicationCommandType.MESSAGE,
)
