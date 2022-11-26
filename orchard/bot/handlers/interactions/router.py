from orchard.bot.handlers.interactions.commands import approve, levelbyid, passcode, ping, sausage, version
from orchard.bot.lib.constants import OptionType
from orchard.bot.lib.slash_commands.slash_router import SlashOption, SlashRoute, SlashRouter


router = SlashRouter(
    routes=[
        SlashRoute(
            name="ping", description="responds with pong!", handler=ping, default_permission=False
        ),
        SlashRoute(
            name="version",
            description="print the version of this bot",
            handler=version,
            default_permission=False
        ),
        SlashRoute(
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
            default_permission=False,
            handler=passcode,
            defer=True,
        ),
        SlashRoute(
            name="levelbyid",
            description="get a level by its id",
            options=[
                SlashOption(
                    type=OptionType.STRING,
                    name="id",
                    description="id of the level",
                    required=True,
                ),
            ],
            default_permission=False,
            handler=levelbyid,
            defer=True,
        ),
        SlashRoute(
            name="plapprove",
            description="get or set the approval value of a level",
            options=[
                SlashOption(
                    type=OptionType.STRING,
                    name="id",
                    description="id of the level",
                    required=True,
                ),
                SlashOption(
                    type=OptionType.INTEGER,
                    name="approval",
                    description="put a value here to set",
                    required=False,
                ),
            ],
            default_permission=False,
            handler=approve,
            defer=True,
        ),
        SlashRoute(
            name="plsausage",
            description="trigger a rescan now!",
            default_permission=False,
            handler=sausage,
            defer=True
        )
    ]
)


