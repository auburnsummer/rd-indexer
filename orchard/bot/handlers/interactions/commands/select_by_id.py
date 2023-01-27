
from orchard.bot.lib.comm.interactor import Interactor
from orchard.bot.lib.entities.level import get_level
from orchard.bot.lib.entities.user import UserHelper
from orchard.bot.lib.utils import get_slash_args
from orchard.db.models import User


async def select_by_id(body, request):
    async with Interactor(body["token"]) as i:
        id = get_slash_args(["id"], body)
        level = await get_level(id)
        user = UserHelper.from_interaction(body)
        # so this actually needs to be a _status_.... hmmm.....
        # user.set_selected_level(level)