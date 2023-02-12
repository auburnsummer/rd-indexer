import logging
from orchard.bot.lib.constants import OptionType
from orchard.bot.lib.slash_commands.slash_router import SlashOption, SlashRoute
from orchard.bot.lib.utils import get_slash_args
from orchard.bot.lib.comm.interactor import Interactor

import orchard.bot.lib.auth.keys as keys
from orchard.bot.lib.comm.message_builder import start_message

logger = logging.getLogger(__name__)


async def _passcode(body, _):
    [check] = get_slash_args(["check"], body)

    async with Interactor(body["token"]) as i:
        if check is not None:
            # branch where we're checking a passcode
            try:
                result = keys.check_passcode(check)
                await i.edit(start_message().content("✅"), "@original")
            except Exception as e:
                logger.info("uhhhhh")
                await i.edit(
                    start_message().content(f"❌: {repr(e)} {str(e)}"), "@original"
                )
        else:
            # branch where we're generating a passcode
            passcode = keys.gen_passcode()

            # only the caller can see the actual passcode, the visible message is an emoji
            await i.edit(start_message().content("🙈"), "@original")

            await i.post(start_message().content(passcode).ephemeral())

passcode = SlashRoute(
    name="plpasscode",
    description="return a passcode for pathlab use (pathlab people only)",
    options=[
        SlashOption(
            type=OptionType.STRING,
            name="check",
            description="put a passcode here to check it",
            required=False,
        )
    ],
    handler=_passcode,
    defer=True,
)