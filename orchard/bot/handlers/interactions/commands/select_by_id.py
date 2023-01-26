
from orchard.bot.lib.comm.interactor import Interactor
from orchard.bot.lib.entities.level import get_level
from orchard.bot.lib.utils import get_slash_args


async def select_by_id(body, request):
    async with Interactor(body["token"]) as i:
        id = get_slash_args(["id"], body)
        level = await get_level(id)