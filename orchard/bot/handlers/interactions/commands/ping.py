from orchard.bot.lib.constants import ResponseType
from starlette.responses import JSONResponse

from orchard.bot.lib.slash_commands.slash_router import SlashRoute


def _ping(body, _):
    return JSONResponse(
        {"type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE, "data": {"content": "pong"}}
    )


ping = SlashRoute(
    name="ping",
    description="responds with pong!",
    handler=_ping,
    default_permission=True,
)
