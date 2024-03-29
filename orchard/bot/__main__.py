import asyncio
import os
import pathlib
import subprocess
from playhouse.sqlite_ext import SqliteExtDatabase
import uvicorn
from orchard.bot.lib.constants import LITESTREAM_ON
from orchard.db.models import Info, Status
from .bot import OrchardBotApp

import sys

import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

db_filename = sys.argv[1]

# run litestream restore
# we're not in async land yet, so this is the normal python subprocess.
if LITESTREAM_ON:
    logger.info("Restoring from litestream now...")
    litestream_path = pathlib.Path(__file__).parent / "litestream.yml"
    env = {**os.environ, "LITESTREAM_DB": sys.argv[1]}
    subprocess.run(
        ["litestream", "restore", "-config", str(litestream_path), sys.argv[1]],
        env=env,
        check=True,
        stdout=sys.stdout,
        stderr=subprocess.STDOUT,
    )


async def start_app():
    db = SqliteExtDatabase(
        sys.argv[1],
        pragmas=[
            ("journal_mode", "wal"),
            ("busy_timeout", 5000),  # https://litestream.io/tips/#busy-timeout
            ("synchronous", "NORMAL"),
        ],
    )
    Status.bind(db)
    Info.bind(db)
    OrchardBotApp.state.db = db
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])
    else:
        port = 8000

    config = uvicorn.Config(
        OrchardBotApp, host="0.0.0.0", port=port, log_level="info", reload=True
    )
    server = uvicorn.Server(config)
    await server.serve()


# todo: this will only work correctly if there's only one worker process.
# for multiple workers (e.g. gunicorn) this will need to be reworked to prevent multiple litestream instances.
# https://litestream.io/tips/#multiple-applications-replicating-into-location-can-corrupt
async def start_litestream():
    logger.info("Beginning litestream replication process...")
    litestream_path = pathlib.Path(__file__).parent / "litestream.yml"
    env = {**os.environ, "LITESTREAM_DB": sys.argv[1]}
    process = await asyncio.create_subprocess_exec(
        "litestream",
        "replicate",
        "-config",
        str(litestream_path),
        env=env,
        stdout=sys.stdout,
        stderr=subprocess.STDOUT,
    )
    try:
        await process.wait()
    except KeyboardInterrupt:
        await process.terminate()


if os.environ.get("ORCHARD_DEBUG"):
    import debugpy

    debugpy.listen(5678)
    debugpy.wait_for_client()  # blocks execution until client is attached


async def main():
    if LITESTREAM_ON:
        # https://textual.textualize.io/blog/2023/02/11/the-heisenbug-lurking-in-your-async-code/
        task1 = start_litestream()
        task2 = start_app()
        await asyncio.gather(task1, task2)
    else:
        task1 = start_app()
        await task1


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Received exit, exiting")
