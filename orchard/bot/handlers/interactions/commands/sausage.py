import httpx
import logging

from orchard.bot.lib.constants import GITHUB_TOKEN
from orchard.bot.lib.comm.interactor import Interactor

from orchard.bot.lib.comm.message_builder import start_message
from orchard.bot.lib.comm import pager
from orchard.bot.lib.slash_commands.slash_router import SlashRoute

SUCCESS_MESSAGE = """
A sausage has been scheduled. See status here: <https://github.com/auburnsummer/rd-indexer/actions>

Note that you will need a GitHub account to view the logs.
"""

logger = logging.getLogger(__name__)


async def _sausage(body, _):
    async with Interactor(body["token"]) as i:
        bid = i.uuid()
        await i.edit(
            start_message()
            .content(
                "Check at <https://github.com/auburnsummer/rd-indexer/actions> that there is no sausage in "
                "process, then press the button."
            )
            .start_button()
            .label("make sausage")
            .uuid(bid)
            .done(),
            "@original",
        )
        await pager.wait(bid)
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.github.com/repos/auburnsummer/rd-indexer/actions/workflows/main.yml/dispatches",
                    json={"ref": "main"},
                    headers={"Authorization": f"token {GITHUB_TOKEN}"},
                )
                resp.raise_for_status()
            await i.edit(
                start_message().content(SUCCESS_MESSAGE).clear_rows(), "@original"
            )
        except Exception as e:
            await i.edit(
                start_message().content(f"An error occurred: {str(e)}").clear_rows(),
                "@original",
            )

sausage = SlashRoute(
    name="plsausage",
    description="trigger a rescan now!",
    default_permission=False,
    handler=_sausage,
    defer=True,
)