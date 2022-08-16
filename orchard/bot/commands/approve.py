import httpx

from orchard.bot.constants import DEFAULT_DB_STATUS_VALUE
from orchard.bot.lib import db
from orchard.bot.lib.db import get_status
from orchard.bot.lib.interactions import Interactor
from orchard.bot.lib.message_builder import MessageBuilder as M, Embed
from orchard.bot.lib.typesense import ts_get_by_id
from orchard.bot.lib.utils import get_slash_args
from orchard.db.models import Status


async def approve(body, request):
    async with Interactor(body["token"]) as i:
        id, approval = get_slash_args(["id", "approval"], body)
        # check this id exists
        try:
            data = await ts_get_by_id(id)
        except httpx.HTTPError:
            # it doesn't exist!
            message = M().content(
                f"😰 I couldn't find a level by the id {id}. Check the spelling. If you're sure this should exist, this might be a bug. ping auburn!"
            )
            await i.edit(message, "@original")
        else:
            # it exists!
            # the typesense API will have approval info, but this might not be up-to-date
            # so we should get approval from our local sqlite db.
            if approval is not None:
                # setting approval route
                db.set_status(id, {'approval': approval})

            local_data = get_status(id)
            message = M()
            embed = (
                Embed()
                    .field("id", id)
                    .field("song", data["song"])
                    .field("authors", str(data["authors"]))
                    .field("approval", local_data.approval)
                    .field("approval_reasons", str(local_data.approval_reasons))
            )
            message.embed(embed)
            await i.edit(message, "@original")
