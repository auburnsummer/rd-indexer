
from orchard.bot.lib.entities.level import get_level
from orchard.bot.lib.entities.status import StatusHelper
from orchard.bot.lib.comm.interactor import Interactor
from orchard.bot.lib.comm.message_builder import MessageBuilder as M, Embed
from orchard.bot.lib.utils import get_slash_args


async def approve(body, request):
    async with Interactor(body["token"]) as i:
        id, approval = get_slash_args(["id", "approval"], body)
        
        level = await get_level(id)
        sh = await StatusHelper.create(id)
        if approval is not None:
            # setting approval route
            sh.set_approval(approval)
            
        local_data = sh.get()
        message = M().embed(
            Embed()
            .field("id", id)
            .field("song", level.song)
            .field("authors", str(level.authors))
            .field("approval", local_data.approval)
            .field("approval_reasons", str(local_data.approval_reasons))
        )
        await i.edit(message, "@original")