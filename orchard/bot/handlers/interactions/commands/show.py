import logging
from orchard.bot.lib.comm.interactor import Interactor
from orchard.bot.lib.entities.level import get_level
from orchard.bot.lib.entities.user import UserHelper
from orchard.bot.lib.utils import get_slash_args
from orchard.bot.lib.comm.message_builder import start_message

logger = logging.getLogger(__name__)


async def show(body, request):
    async with Interactor(body["token"]) as i:
        user = UserHelper.from_interaction(body)
        if user.get().selected_level is not None:
            level = await get_level(user.get().selected_level.id)
            message = (
                start_message()
                .start_embed()
                .author(level.artist, level.icon)
                .title(level.song)
                .description(level.description)
                .field("Authors", ", ".join(level.authors), True)
                .field("Difficulty", level.difficulty, True)
                .field("Tags", ", ".join(level.tags), True)
                .image(level.image)
                .done()
            )
            await i.edit(message, "@original")
        else:
            await i.edit(
                start_message().content(
                    "You don't have a level selected. Use the `/search` command to select a level before using this command."
                ),
                "@original",
            )
