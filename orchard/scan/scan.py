from io import BytesIO
import logging
import sys
from sqlite_utils import Database
from orchard.scan.b2 import upload

from orchard.scan.schema import make_schema, OrchardDatabase
from orchard.scan.sources.old_sheet import OldSheetScraper
from orchard.vitals import analyze
import traceback


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

CODEX = "https://codex.rhythm.cafe"


def main(db: Database):
    sources = [("yeoldesheet", OldSheetScraper)]

    if "level" not in db.table_names():
        logger.info("The DB doesn't contain a 'level' table. Making it now...")
        make_schema(db)

    orchard = OrchardDatabase(db)

    for source_id, scraper_class in sources:
        # Initiate the scraper and get the current list of iids.
        scraper = scraper_class()
        logger.info(f"Beginning scrape for source {source_id}...")
        iids = scraper.get_iids()
        logger.info(f"{len(iids)} iids found.")

        # Calculate the diff between the db's current iids and the given list.
        current_set = orchard.get_source_set(source_id)
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
                buf = scraper.download_iid(iid)
                file = BytesIO(buf)

                # Run vitals on the file.
                vit = analyze(file)
                logger.info(
                    f"it's {vit['song']} by {','.join(vit['authors'])}, id: {vit['id']}"
                )

                # Does this id already exist? This could happen if the same level is in multiple sources.
                if orchard.does_level_exist(vit["id"]):
                    logger.info("this level already exists in the db. Bailing out now.")
                    continue

                # upload to b2
                image_url = f"{vit['id']}.png"
                thumbnail_url = f"{vit['id']}_thumbnail.png"
                rdzip_url = f"{vit['id']}.rdzip"
                icon_url = f"{vit['id']}_icon.png"

                to_upload = {
                    image_url: vit["image"],
                    thumbnail_url: vit["thumb"],
                    rdzip_url: file,
                }
                if vit["icon"]:
                    to_upload[icon_url] = vit["icon"]

                upload(to_upload)

                # Add to database.
                to_add = {
                    "url": scraper.get_url(iid),  # even if this is None that's fine
                    "url2": f"{CODEX}/{rdzip_url}",
                    "image": f"{CODEX}/{image_url}",
                    "thumb": f"{CODEX}/{thumbnail_url}",
                    "icon": f"{CODEX}/{icon_url}",
                    "source": source_id,
                    "source_iid": iid,
                }

                if vit["icon"]:
                    to_add["icon"] = f"{CODEX}/{icon_url}"

                orchard.add_level({**vit, **to_add})

            except Exception as e:
                logger.info(f"Error when processing iid {iid}: {e}")
                logger.info(traceback.format_exc())

        for index, iid in enumerate(iids_to_delete):
            logger.info(f"Deleting iid {iid} ({index+1} / {len(iids_to_delete)})")
            orchard.delete_level(source_id, iid)


if __name__ == "__main__":
    db = Database(sys.argv[1])
    main(db)
