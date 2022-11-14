import sys
from collections import defaultdict

import uvicorn
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from playhouse.sqlite_ext import SqliteExtDatabase

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route

import orchard.bot.lib.crosscode as crosscode

import orchard.bot.commands as commands
from orchard.bot.lib.constants import (
    OptionType,
    PUBLIC_KEY,
    ResponseType,
)
from orchard.bot.lib.register import (
    update_slash_commands
)

from orchard.bot.lib.slash_router import (
    SlashOption,
    SlashRoute,
    SlashRouter,
)

from orchard.bot import handlers

# All the routes we're using go here.
from orchard.db.models import Status

router = SlashRouter(
    routes=[
        SlashRoute(
            name="ping", description="responds with pong!", handler=commands.ping, default_permission=False
        ),
        SlashRoute(
            name="version",
            description="print the version of this bot",
            handler=commands.version,
            default_permission=False
        ),
        SlashRoute(
            name="plpasscode",
            description="return a passcode for pathlab use (pathlab people only)",
            options=[
                SlashOption(
                    type=OptionType.STRING,
                    name="check",
                    description="put a passcode here to check it",
                    required=False,
                )
            ],
            default_permission=False,
            handler=commands.passcode,
            defer=True,
        ),
        SlashRoute(
            name="levelbyid",
            description="get a level by its id",
            options=[
                SlashOption(
                    type=OptionType.STRING,
                    name="id",
                    description="id of the level",
                    required=True,
                ),
            ],
            default_permission=False,
            handler=commands.levelbyid,
            defer=True,
        ),
        SlashRoute(
            name="plapprove",
            description="get or set the approval value of a level",
            options=[
                SlashOption(
                    type=OptionType.STRING,
                    name="id",
                    description="id of the level",
                    required=True,
                ),
                SlashOption(
                    type=OptionType.INTEGER,
                    name="approval",
                    description="put a value here to set",
                    required=False,
                ),
            ],
            default_permission=False,
            handler=commands.approve,
            defer=True,
        ),
        SlashRoute(
            name="plsausage",
            description="trigger a rescan now!",
            default_permission=False,
            handler=commands.sausage,
            defer=True
        )
    ]
)


async def interaction_handler(request):
    """
    Starlette handler for the /interactions endpoint.
    """
    # Check the headers are correct: https://discord.com/developers/docs/interactions/slash-commands#security-and-authorization
    verify_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(PUBLIC_KEY))

    rheaders = defaultdict(str, request.headers)
    signature = rheaders["x-signature-ed25519"]

    timestamp = rheaders["x-signature-timestamp"]
    payload = await request.body()
    # concat bytes together
    to_verify = timestamp.encode('ascii') + payload

    try:
        verify_key.verify(bytes.fromhex(signature), to_verify)
    except InvalidSignature:
        return JSONResponse({"error": "Invalid request signature"}, status_code=401)

    # If we've gotten here, headers are valid. now respond...
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


async def prerun_update_slash_commands():
    """
    Before launching, update the slash commands defined by the router to the discord API.
    This is done by calling /commands. note that bot can no longer update their own
    permissions in permissions v2.
    """
    print("updating slash commands...")
    payload = router.api()
    # print(payload)
    resp = (await update_slash_commands(payload)).json()
    # print(resp)
    print("done!")


async def prerun_check_db():
    db = app.state.db
    if not db.table_exists("status"):
        print("Status table not found, making it now...")
        db.create_tables([Status])


# two identical routes. this is so i can change it in discord developer options to check
# we are handling ping and auth correctly.
app = Starlette(
    debug=True,
    routes=[
        Route("/interactions", interaction_handler, methods=["POST"]),
        Route("/interactions2", interaction_handler, methods=["POST"]),
        Route('/approval/{id}', handlers.set_approval, methods=['POST', 'GET']),
        Route('/multi/approval', handlers.get_approval_multi, methods=['POST'])
    ],
    on_startup=[
        prerun_update_slash_commands,
        prerun_check_db,
    ],
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ],
)
