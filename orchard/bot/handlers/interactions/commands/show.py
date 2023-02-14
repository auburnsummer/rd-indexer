import json
import logging
from orchard.db.models import Level
from orchard.bot.lib.comm.interactor import Interactor
from orchard.bot.lib.constants import OptionType
from orchard.bot.lib.entities.level import get_level
from orchard.bot.lib.entities.user import UserHelper
from orchard.bot.lib.slash_commands.slash_router import (
    RouteType,
    SlashOption,
    SlashOptionChoice,
    SlashRoute,
)
from orchard.bot.lib.utils import get_slash_args
from orchard.bot.lib.comm.message_builder import start_message
from datetime import datetime

from typing import List

from playhouse.shortcuts import model_to_dict

logger = logging.getLogger(__name__)

# not the same as in difficulty_facet.py
DIFFICULTIES = ["Easy", "Medium", "Tough", "Very Tough"]


def tag_string(tags: List[str]):
    return ", ".join(f"[{tag}]" for tag in tags)


def beat_type_string(lev: Level):
    pairs = [
        (lev.has_classics, "Classics"),
        (lev.has_oneshots, "Oneshots"),
        (lev.has_holds, "Holds"),
        (lev.has_freetimes, "Freetimes"),
        (lev.has_freezeshots, "Freezeshots"),
        (lev.has_skipshots, "Skipshots"),
        (lev.has_squareshots, "Squareshots"),
    ]
    return ", ".join(name for condition, name in pairs if condition)


def bpm_string(lev: Level):
    if lev.max_bpm == lev.min_bpm:
        return f"{lev.max_bpm} BPM"
    return f"{lev.min_bpm}-{lev.max_bpm} BPM"


def player_string(lev: Level):
    pairs = [(lev.single_player, "1P"), (lev.two_player, "2P")]
    return ", ".join(name for condition, name in pairs if condition)


def window_dance_string(lev: Level):
    return "Yes" if lev.has_window_dance else "No"


def level_embed_default(level: Level):
    return (
        start_message()
        .start_embed()
        .author(level.artist, level.icon)
        .title(level.song)
        .description(level.description)
        .field("Authors", ", ".join(level.authors), True)
        .field("Difficulty", DIFFICULTIES[level.difficulty], True)
        .field("Tags", tag_string(level.tags), True)
        .image(level.image)
        .done()
    )


def level_embed_detailed(level: Level):
    return (
        start_message()
        .start_embed()
        .author(level.artist, level.icon)
        .title(level.song)
        .description(level.description)
        .field("Authors", ", ".join(level.authors), True)
        .field("Difficulty", DIFFICULTIES[level.difficulty], True)
        .field("Tags", tag_string(level.tags), True)
        .field("Beat Types", beat_type_string(level), True)
        .field("BPM", bpm_string(level), True)
        .field("Syringe Hue", f"{level.hue}", True)
        .field("Players", player_string(level), True)
        .field("Window Dance", window_dance_string(level), True)
        .image(level.image)
        .done()
    )


def level_embed_blend(level: Level):
    return (
        start_message()
        .start_embed()
        .author(f"Daily Blend: {datetime.now().strftime('%a, %B %d %Y')}")
        .field("Level", level.song, True)
        .field("Authors", ", ".join(level.authors), True)
        .field("Description", level.description, False)
        .field("Tags", tag_string(level.tags), False)
        .field("Modes", player_string(level), True)
        .field("Download", f"[Link]({level.url or level.url2})", True)
        .image(level.image)
        .done()
        .start_embed()
        .author("About the Daily Blend Café")
        .description(
            "The Daily Blend Café is like a book club for custom levels! Play the daily level and post your score (enable Detailed Level Results in Advanced Settings), and leave a comment with what you liked about the level!"
        )
        .done()
    )


def level_embed_json(level: Level):
    j = json.dumps(model_to_dict(level), ensure_ascii=False, indent=2)
    return start_message().content(f"```\n{j}\n```")


async def _show(body, request):
    async with Interactor(body["token"]) as i:
        [style] = get_slash_args(["style"], body)
        user = UserHelper.from_interaction(body)
        if user.get().selected_level is not None:
            level = await get_level(user.get().selected_level.id)
            func = {
                "default": level_embed_default,
                "details": level_embed_detailed,
                "blend": level_embed_blend,
                "json": level_embed_json,
            }[style]
            message = func(level)
            # nb: when editing the original message, ephemerality depends on the initial ACK
            await i.edit(message, "@original")
        else:
            await i.edit(
                start_message().content(
                    "You don't have a level selected. Use the `/search` command to select a level before using this command."
                ),
                "@original",
            )


def _defer(body, request):
    [private] = get_slash_args(["private"], body)
    return RouteType.DEFER_EPHEMERAL if private else RouteType.DEFER_VISIBLE


show = SlashRoute(
    name="print",
    description="Show the selected level.",
    default_permission=True,
    options=[
        SlashOption(
            type=OptionType.BOOLEAN,
            name="private",
            description="Only show the level to you.",
            required=False,
        ),
        SlashOption(
            type=OptionType.STRING,
            name="style",
            description="style of embed to use",
            required=False,
            choices=[
                SlashOptionChoice("Default", "default"),
                SlashOptionChoice("More details", "details"),
                SlashOptionChoice("Daily Blend", "blend"),
                SlashOptionChoice("JSON", "json"),
            ],
        ),
    ],
    handler=_show,
    defer=_defer,
)
