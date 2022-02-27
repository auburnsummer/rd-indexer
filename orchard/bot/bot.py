import logging
import sys
from collections import defaultdict

import uvicorn
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey
from sqlite_utils import Database
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route

import orchard.bot.crosscode as crosscode
import orchard.bot.commands as commands
from orchard.bot.constants import PATHLAB_ROLE, OptionType, PUBLIC_KEY, PermissionType, ResponseType
from orchard.bot.register import get_command_to_id_mapping, update_slash_commands, update_slash_permissions
from orchard.bot.schema import make_schema
from orchard.bot.slash_router import SlashOption, SlashOptionPermission, SlashRoute, SlashRouter

from orchard.bot import handlers

# All the routes we're using go here.
router = SlashRouter(routes=[
    SlashRoute(name='ping', description='responds with pong!', handler=commands.ping),
    SlashRoute(name='version', description='print the version of this bot', handler=commands.version),
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
        name='levelbyid',
        description='get a level by its id',
        options=[
            SlashOption(type=OptionType.STRING, name="id", description="id of the level", required=True),
        ],
        default_permission=True,
        handler=commands.levelbyid,
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
        return router.handle(body, request)

    # handle components (button clicks, etc...)
    # under our model, all components are per-interaction (we don't have "permanent" buttons)
    if body['type'] == 3:
        return await crosscode.handle(body)

    # usually we shouldn't reach here
    print(body)
    return JSONResponse({'hello': 'world'})


async def prerun_update_slash_commands():
    """
    Before launching, update the slash commands defined by the router to the discord API.
    This has to be done in two steps, calling the /commands and then /commands/permissions
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

async def prerun_check_db():
    db = app.state.db
    if 'status' not in db.table_names():
        print("Status table not found, making it now...")
        make_schema(db)

# two identical routes. this is so i can change it in discord developer options to check
# we are handling ping and auth correctly.
app = Starlette(debug=True, routes=[
    Route('/interactions', interaction_handler, methods=['POST']),
    Route('/interactions2', interaction_handler, methods=['POST']),
    Route('/status.db', handlers.status_dot_db, methods=['GET']),
    # Route('/approval/{id}', handlers.set_approval, methods=['POST', 'GET'])
], on_startup=[
    prerun_update_slash_commands,
    prerun_check_db,
], middleware=[
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
])

# Discord requires HTTPS. Suggest using a localhost https proxy such as ngrok
# e.g. run separately: ngrok http 8000
if __name__ == '__main__':
    db = Database(sys.argv[1])
    app.state.db = db
    uvicorn.run(app, host='0.0.0.0', port=8000)