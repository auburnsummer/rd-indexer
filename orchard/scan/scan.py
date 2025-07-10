import asyncio
from io import BytesIO
import logging
import os
import sys

from playhouse.sqlite_ext import SqliteExtDatabase

from orchard.db.models import Level, Info
from orchard.scan.b2 import upload

from orchard.scan.db_funcs import get_source_set, level_exists, add_level, delete_level
from orchard.scan.sources.old_sheet import OldSheetScraper
from orchard.vitals import analyze
import traceback
import yaml
from playhouse.migrate import *
from peewee import *

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

CODEX = "https://codex.rhythm.cafe"

SCRAPER_MAP = {"OldSheetScraper": OldSheetScraper}

def migrate_0_1(db: SqliteExtDatabase):
    migrator = SqliteMigrator(db)
    migrate(
        migrator.add_column('level', 'rd_md5', TextField(null=True))
    )

async def main(db: SqliteExtDatabase, sources):
    Level.bind(db)
    Info.bind(db)

    if not db.table_exists("level"):
        logger.info("The DB doesn't contain a 'level' table. Making it now...")
        db.create_tables([Level])

    if not db.table_exists("info"):
        logger.info("MIGRATE 0 -> 1")
        migrate_0_1(db)
        db.create_tables([Info])
        Info.create(id=0, schema_version=1)

    for source_id, scraper_class, kwargs in sources:
        # Initiate the scraper and get the current list of iids.
        scraper = scraper_class(**kwargs)
        logger.info(f"Beginning scrape for source {source_id}...")
        iids = await scraper.get_iids()
        logger.info(f"{len(iids)} iids found.")

        # Calculate the diff between the db's current iids and the given list.
        current_set = get_source_set(source_id)
        our_set = set(iids)

        iids_to_add = our_set - current_set
        iids_to_delete = current_set - our_set

        logger.info(
            f"Adding {len(iids_to_add)} iids, removing {len(iids_to_delete)} iids"
        )

        # start adding iids.
        for index, iid in enumerate(iids_to_add):
            try:
                logger.info(f"Processing iid {iid}... ({index+1} / {len(iids_to_add)})")
                # Download the level and wrap it in a file object.
                buf = await scraper.download_iid(iid)
                file = BytesIO(buf)

                # Run vitals on the file.
                vit = analyze(file)
                logger.info(
                    f"it's {vit['song']} by {','.join(vit['authors'])}, id: {vit['id']}"
                )

                # Does this id already exist? This could happen if the same level is in multiple sources.
                if level_exists(vit["id"]):
                    logger.info("this level already exists in the db. Bailing out now.")
                    continue

                # upload to b2
                image_url = f"{vit['id']}.png"
                thumbnail_url = f"{vit['id']}_thumbnail.png"
                rdzip_url = f"{vit['id']}.rdzip"
                icon_url = f"{vit['id']}_icon.png"

                to_upload = {
                    rdzip_url: file,
                    image_url: vit["image"],
                    thumbnail_url: vit["thumb"],
                }
                if vit["icon"]:
                    to_upload[icon_url] = vit["icon"]

                upload(to_upload)

                # Add to database.
                to_add = {
                    "url": await scraper.get_url(
                        iid
                    ),  # even if this is None that's fine
                    "url2": f"{CODEX}/{rdzip_url}",
                    "image": f"{CODEX}/{image_url}",
                    "thumb": f"{CODEX}/{thumbnail_url}",
                    "icon": f"{CODEX}/{icon_url}",
                    "source": source_id,
                    "source_iid": iid,
                    "source_metadata": await scraper.get_metadata(iid),
                }

                if vit["icon"]:
                    to_add["icon"] = f"{CODEX}/{icon_url}"

                level = {**vit, **to_add}
                add_level(level)
                await scraper.on_index(level)

            except Exception as e:
                logger.info(f"Error when processing iid {iid}: {e}")
                logger.info(traceback.format_exc())

        for index, iid in enumerate(iids_to_delete):
            logger.info(f"Deleting iid {iid} ({index+1} / {len(iids_to_delete)})")
            delete_level(source_id, iid)
            await scraper.on_delete(iid)


if __name__ == "__main__":
    if os.environ.get("ORCHARD_DEBUG"):
        import debugpy

        debugpy.listen(5678)
        debugpy.wait_for_client()  # blocks execution until client is attached
    database_file_name = sys.argv[1]
    sources_file_name = sys.argv[2]
    db = SqliteExtDatabase(database_file_name)
    with open(sources_file_name, "r") as f:
        loaded_sources = yaml.load(f.read(), Loader=yaml.Loader)

    db.connect()
    asyncio.run(main(db, loaded_sources))
