
import logging
from orchard.bot.lib.comm.interactor import Interactor
from orchard.bot.lib.entities.level import get_level
from orchard.bot.lib.entities.status import StatusHelper
from orchard.bot.lib.entities.user import UserHelper
from orchard.bot.lib.utils import get_slash_args
from orchard.db.models import User
from orchard.bot.lib.comm.message_builder import MessageBuilder as M

logger = logging.getLogger(__name__)

async def select_by_id(body, request):
    async with Interactor(body["token"]) as i:
        id_to_select, = get_slash_args(["id"], body)
        logger.warn("1")
        user = UserHelper.from_interaction(body)
        logger.warn("2")
        sh = await StatusHelper.create(id_to_select)
        logger.warn("3")
        user.set_selected_level(sh.get())
        logger.warn("4")
        level = await get_level(id)
        logger.warn("5")
        message = M() \
            .content(f"Selected level is set to {level.song} by {level.authors} (id: {level.id})")
        await i.edit(message, "@original")