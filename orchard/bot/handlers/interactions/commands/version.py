from orchard.bot.lib.constants import ResponseType, BOT_VERSION
from starlette.responses import JSONResponse
from orchard.bot.lib.comm.message_builder import start_message


def version(body, _):
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
