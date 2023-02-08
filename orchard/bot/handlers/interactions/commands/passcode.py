import logging
from orchard.bot.lib.utils import get_slash_args
from orchard.bot.lib.comm.interactor import Interactor

import orchard.bot.lib.auth.keys as keys
from orchard.bot.lib.comm.message_builder import MessageBuilder as M

logger = logging.getLogger(__name__)


async def passcode(body, _):
    [check] = get_slash_args(["check"], body)

    async with Interactor(body["token"]) as i:
        if check is not None:
            # branch where we're checking a passcode
            try:
                result = keys.check_passcode(check)
                await i.edit(M().content("✅"), "@original")
            except Exception as e:
                logger.info("uhhhhh")
                await i.edit(M().content(f"❌: {repr(e)} {str(e)}"), "@original")
        else:
            # branch where we're generating a passcode
            passcode = keys.gen_passcode()

            # only the caller can see the actual passcode, the visible message is an emoji
            await i.edit(M().content("🙈"), "@original")

            await i.post(M().content(passcode).ephemeral())
