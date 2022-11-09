from orchard.bot.lib.constants import ResponseType
from starlette.responses import JSONResponse

from orchard.bot.lib.utils import get_slash_args


def add(body, _):
    a, b = get_slash_args(["a", "b"], body)
    out = f"{a + b}"
    return JSONResponse(
        {"type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE, "data": {"content": out}}
    )
