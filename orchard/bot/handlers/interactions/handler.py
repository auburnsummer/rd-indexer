from orchard.bot.lib.comm import crosscode
from orchard.bot.lib.auth.discord_public_key import with_discord_public_key_verification
from orchard.bot.lib.constants import ResponseType
from starlette.responses import JSONResponse

from .router import router

@with_discord_public_key_verification
async def interaction_handler(request):
    """
    Starlette handler for the /interactions endpoint.
    """
    body = await request.json()

    # handle ping event...
    if body["type"] == 1:
        return JSONResponse({"type": ResponseType.PONG})

    # handle slash commands...
    if body["type"] == 2:
        return router.handle(body, request)

    # handle components (button clicks, etc...)
    # under our model, all components are per-interaction (we don't have "permanent" buttons)
    if body["type"] == 3:
        return await crosscode.handle(body)

    # usually we shouldn't reach here
    print(body)
    return JSONResponse({"hello": "world"})