from orchard.bot.handlers.interactions.commands import (
    approve,
    passcode,
    ping,
    sausage,
    show,
    version,
    select_by_id,
)
from orchard.bot.lib.slash_commands.slash_router import SlashRouter

router = SlashRouter(
    routes=[ping, version, passcode, approve, sausage, select_by_id, show]
)
