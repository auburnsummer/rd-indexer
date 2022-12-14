import httpx

from orchard.bot.lib.constants import DEFAULT_DB_STATUS_VALUE
from orchard.bot.lib.entities import status
from orchard.bot.lib.entities.status import get_status
from orchard.bot.lib.comm.interactor import Interactor
from orchard.bot.lib.comm.message_builder import MessageBuilder as M, Embed
from orchard.bot.lib.ext.datasette import datasette_request
from orchard.bot.lib.utils import get_slash_args
from orchard.db.models import Status, Level


async def approve(body, request):
    async with Interactor(body["token"]) as i:
        id, approval = get_slash_args(["id", "approval"], body)
        # check this id exists
        level = datasette_request(Level.select().where(Level.id == id))
        if level:
            level = level[0]
            # it exists!
            # the level table does not contain approval, so...
            if approval is not None:
                # setting approval route
                status.set_status(id, {'approval': approval})
            
            local_data = get_status(id)
            message = M().embed(
                Embed()
                .field("id", id)
                .field("song", level.song)
                .field("authors", str(level.authors))
                .field("approval", local_data.approval)
                .field("approval_reasons", str(local_data.approval_reasons))
            )
            await i.edit(message, "@original")

        else:
            # it doesn't exist!
            message = M().content(
                f"😰 I couldn't find a level by the id {id}. Check the spelling. If you're sure this should exist, this might be a bug. ping auburn!"
            )
            await i.edit(message, "@original")