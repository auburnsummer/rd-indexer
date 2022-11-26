import httpx

from orchard.bot.lib.constants import GITHUB_TOKEN
from orchard.bot.lib.comm.interactor import Interactor

from orchard.bot.lib.comm.message_builder import MessageBuilder as M, ActionRow, Button
import orchard.bot.lib.comm.crosscode as cc

SUCCESS_MESSAGE = """
A sausage has been scheduled. See status here: <https://github.com/auburnsummer/rd-indexer/actions>

Note that you will need a GitHub account to view the logs.
"""


async def sausage(body, _):
    async with Interactor(body["token"]) as i:
        bid = await i.uuid()
        await i.edit(
            M()
                .content("Check at <https://github.com/auburnsummer/rd-indexer/actions> that there is no sausage in "
                         "process, then press the button.")
                .row(
                    ActionRow(
                        Button(label="make sausage", custom_id=bid)
                    )
                )
            ,
            "@original"
        )
        await cc.button_press(bid)
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.github.com/repos/auburnsummer/rd-indexer/actions/workflows/main.yml/dispatches",
                    json={
                        "ref": "main"
                    },
                    headers={
                        "Authorization": f"token {GITHUB_TOKEN}"
                    }
                )
                resp.raise_for_status()
            await i.edit(
                M().content(SUCCESS_MESSAGE).clear_rows(),
                "@original"
            )
        except Exception as e:
            await i.edit(
                M().content(f"An error occurred: {str(e)}").clear_rows(),
                "@original"
            )