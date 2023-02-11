from orchard.bot.lib.entities.level import get_level
from orchard.bot.lib.entities.status import StatusHelper
from orchard.bot.lib.comm.interactor import Interactor
from orchard.bot.lib.comm.message_builder import start_message
from orchard.bot.lib.utils import get_slash_args


async def approve(body, request):
    async with Interactor(body["token"]) as i:
        id, approval = get_slash_args(["id", "approval"], body)  # type: ignore

        level = await get_level(id)
        sh = await StatusHelper.create(id)
        if approval is not None:
            # setting approval route
            sh.set_approval(approval)

        local_data = sh.get()
        await i.edit(
            start_message()
            .start_embed()
            .field("id", id)
            .field("song", level.song)
            .field("authors", str(level.authors))
            .field("approval", local_data.approval)
            .done(),
            "@original",
        )
