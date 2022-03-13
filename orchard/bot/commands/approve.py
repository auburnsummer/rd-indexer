import httpx

from orchard.bot import db
from orchard.bot.interactions import Interactor
from orchard.bot.message_builder import MessageBuilder as M, Embed
from orchard.bot.typesense import get_by_id
from orchard.bot.utils import get_slash_args


async def approve(body, request):
    async with Interactor(body["token"]) as i:
        id, approval = get_slash_args(["id", "approval"], body)
        # check this id exists
        try:
            data = await get_by_id(id)
        except httpx.HTTPError:
            message = M().content(
                f"😰 I couldn't find a level by the id {id}. Check the spelling. If you're sure this should exist, this might be a bug. ping auburn!"
            )
            await i.edit(message, "@original")
        else:
            # the typesense API will have approval info, but this might not be up-to-date
            if approval is None:
                # getting approval route
                pass
            else:
                # setting approval route
                db.set_status(request.app.state.db, id, {'approval': approval})
            local_data = db.get_or_default(request.app.state.db, id)
            message = M()
            embed = (
                Embed()
                    .field("id", id)
                    .field("song", data["song"])
                    .field("authors", str(data["authors"]))
                    .field("approval", local_data["approval"])
                    .field("approval_reasons", str(local_data["approval_reasons"]))
            )
            message.embed(embed)
            await i.edit(message, "@original")


