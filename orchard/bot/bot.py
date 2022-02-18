import httpx

from collections import defaultdict

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from orchard.bot.slash_router import SlashOption, SlashOptionPermission, SlashRoute, SlashRouter
from orchard.bot.constants import DB_PATH, DB_URL, PATHLAB_ROLE, OptionType, PUBLIC_KEY, PermissionType, ResponseType
from orchard.bot.register import get_command_to_id_mapping, update_slash_commands, update_slash_permissions
from pathlib import Path

from orchard.bot import commands as commands
import orchard.bot.handlers as handlers
import orchard.bot.crosscode as crosscode

# All the routes we're using go here.
router = SlashRouter(routes=[
    SlashRoute(name='ping', description='responds with pong!', handler=commands.ping),
    SlashRoute(
        name='plpasscode',
        description='return a passcode for pathlab use (pathlab people only)',
        options=[
            SlashOption(type=OptionType.STRING, name="check", description="put a passcode here to check it", required=False)
        ],
        permissions=[
            SlashOptionPermission(id=PATHLAB_ROLE, type=PermissionType.ROLE, permission=True)
        ],
        default_permission=False,
        handler=commands.passcode,
        defer=True
    ),
    SlashRoute(
        name='plapprove',
        description='get or set the approval value of a level',
        options=[
            SlashOption(type=OptionType.STRING, name="id", description="id of the level", required=True),
            SlashOption(type=OptionType.INTEGER, name="approval", description="put a value here to set", required=False)
        ],
        permissions=[
            SlashOptionPermission(id=PATHLAB_ROLE, type=PermissionType.ROLE, permission=True)
        ],
        default_permission=False,
        handler=commands.approve,
        defer=True
    )
])

async def interaction_handler(request):
    """
    Starlette handler for the /interactions endpoint.
    """
    # Check the headers are correct: https://discord.com/developers/docs/interactions/slash-commands#security-and-authorization
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    rheaders = defaultdict(str, request.headers)
    signature = rheaders["x-signature-ed25519"]
    timestamp = rheaders["x-signature-timestamp"]
    payload = await request.body()

    try:
        verify_key.verify(timestamp.encode() + payload, bytes.fromhex(signature))
    except BadSignatureError:
        return JSONResponse({'error': 'Invalid request signature'}, status_code=401)

    # If we've gotten here, headers are valid. now respond...
    body = await request.json()

    # handle ping event...
    if body['type'] == 1:
        return JSONResponse({'type' : ResponseType.PONG})

    # handle slash commands...
    if body['type'] == 2:
        return router.handle(body)

    # handle components (button clicks, etc...)
    # under our model, all components are per-interaction (we don't have "permanent" buttons)
    if body['type'] == 3:
        return await crosscode.handle(body)
    
    print(body)
    return JSONResponse({'hello': 'world'})


async def prerun_update_slash_commands():
    """
    Before launching, update the slash commands defined by the router.  
    """
    print("updating slash commands...")
    payload = router.api()
    print(payload)
    resp = (await update_slash_commands(payload)).json()
    print(resp)

    mapping = get_command_to_id_mapping(resp)
    print("updating permissions...")
    payload2 = router.permission_api(mapping)
    print(payload2)
    print((await update_slash_permissions(payload2)).json())
    print("done!")


# two identical routes. this is so i can change it in discord developer options to check
# we are handling ping and auth correctly.
app = Starlette(debug=True, routes=[
    Route('/interactions', interaction_handler, methods=['POST']),
    Route('/interactions2', interaction_handler, methods=['POST']),
    # Route('/orchard.db', handlers.orchard_dot_db, methods=['GET']),
    # Route('/approval/{id}', handlers.set_approval, methods=['POST', 'GET'])
], on_startup=[
    prerun_update_slash_commands
], middleware=[
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
])

# Discord requires HTTPS. Suggest using a localhost https proxy such as ngrok
# e.g. run seperately: ngrok http 8000
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)