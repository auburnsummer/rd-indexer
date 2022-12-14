from orchard.bot.lib.constants import ResponseType
from starlette.responses import JSONResponse


def ping(body, _):
    return JSONResponse(
        {"type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE, "data": {"content": "pong"}}
    )
