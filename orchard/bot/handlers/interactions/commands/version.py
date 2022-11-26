from orchard.bot.lib.constants import ResponseType, BOT_VERSION
from starlette.responses import JSONResponse
from orchard.bot.lib.comm.message_builder import MessageBuilder as M, Embed


def version(body, _):
    resp = M().embed(Embed().title("CLC Version").description(BOT_VERSION))
    return JSONResponse(
        {"data": resp.payload(), "type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE}
    )
