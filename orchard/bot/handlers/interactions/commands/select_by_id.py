import logging
from orchard.bot.lib.comm.interactor import Interactor
from orchard.bot.lib.constants import OptionType
from orchard.bot.lib.entities.level import get_level
from orchard.bot.lib.entities.status import StatusHelper
from orchard.bot.lib.entities.user import UserHelper
from orchard.bot.lib.slash_commands.slash_router import (
    RouteType,
    SlashOption,
    SlashRoute,
)
from orchard.bot.lib.utils import get_slash_args
from orchard.db.models import User
from orchard.bot.lib.comm.message_builder import start_message

logger = logging.getLogger(__name__)


async def _select_by_id(body, request):
    async with Interactor(body["token"]) as i:
        (id_to_select,) = get_slash_args(["id"], body)
        user = UserHelper.from_interaction(body)
        sh = await StatusHelper.create(id_to_select)

        user.set_selected_level(sh.get())
        level = await get_level(id_to_select)

        message = start_message().content(
            f"Selected level is set to {level.song} by {','.join(level.authors)} (id: {level.id})"
        )
        await i.delete("@original")
        await i.post(message.ephemeral())


select_by_id = SlashRoute(
    name="select_by_id",
    description="Select a level",
    options=[
        SlashOption(
            type=OptionType.STRING,
            name="id",
            description="id of the level to select",
            required=True,
        )
    ],
    default_permission=True,
    handler=_select_by_id,
    defer=RouteType.DEFER_VISIBLE,
)
