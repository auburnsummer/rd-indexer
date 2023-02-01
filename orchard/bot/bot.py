from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route
from orchard.bot.handlers.interactions.router import router
from orchard.bot.handlers.interactions.handler import interaction_handler
from orchard.bot.handlers.set_approval import set_approval
from orchard.bot.handlers.get_approval_multi import get_approval_multi

from orchard.bot.lib.slash_commands.register import (
    update_slash_commands
)

# All the routes we're using go here.
from orchard.db.models import Info, Status, User

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
    db = OrchardBotApp.state.db
    if not db.table_exists("status"):
        print("Status table not found, making it now...")
        db.create_tables([Status])
    if not db.table_exists("info"):
        print("Info table not found, making it now.")
        db.create_tables([Info])
        Info.create(id=0, schema_version=1)
    if not db.table_exists("user"):
        print("User table not found, making it now.")
        db.create_tables([User])


# two identical routes. this is so i can change it in discord developer options to check
# we are handling ping and auth correctly.
OrchardBotApp = Starlette(
    debug=True,
    routes=[
        Route("/interactions", interaction_handler, methods=["POST"]),
        Route("/interactions2", interaction_handler, methods=["POST"]),
        Route('/approval/{id}', set_approval, methods=['POST', 'GET']),
        Route('/multi/approval', get_approval_multi, methods=['POST'])
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
