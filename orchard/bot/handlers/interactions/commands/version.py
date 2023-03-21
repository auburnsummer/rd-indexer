from orchard.bot.lib.constants import ResponseType, BOT_VERSION
from starlette.responses import JSONResponse
from orchard.bot.lib.comm.message_builder import start_message
from orchard.bot.lib.slash_commands.slash_router import SlashRoute


def _version(body, _):
    message = (
        start_message()
        .start_embed()
        .title("CLC Version")
        .description(BOT_VERSION)
        .done()
    )
    return JSONResponse(
        {"data": message.payload(), "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE}
    )


version = SlashRoute(
    name="version", description="print the version of this bot", handler=_version, default_permission=True
)
