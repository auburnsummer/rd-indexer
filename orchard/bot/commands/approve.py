from orchard.bot.interactions import Interactor
from orchard.bot.message_builder import MessageBuilder as M
from orchard.bot.utils import get_slash_args
from orchard.bot.db import get_status, set_status


async def approve(body):
    async with Interactor(body["token"]) as i:
        id, approval = get_slash_args(['id', 'approval'], body)
        if approval is None:
            # getting an approval route
            row = await get_status(id)
            if row is not None:
                message = M() \
                    .content(f"{row['id']}: {row['approval']}")
            else:
                message = M().content(f"😰 I couldn't find a level by the id {id}. Check the spelling. If you're sure this should exist, this might be a bug. ping auburn!")
            await i.edit(message, "@original")
        else:
            await set_status(id, {'approval': approval})
            await i.edit(M().content(f"id {id} set to {approval}"), "@original")