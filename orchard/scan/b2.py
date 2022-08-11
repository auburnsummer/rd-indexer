import logging

import httpx
from dotenv import load_dotenv
import os
from b2sdk.v2 import *
from b2sdk import exception

logger = logging.getLogger(__name__)

load_dotenv()

BUCKET_NAME = "rdcodex"

if "KEY_ID" in os.environ and "B2_ACCESS_KEY" in os.environ:
    b2_authenticated = True
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    b2_api.authorize_account(
        "production", os.environ["KEY_ID"], os.environ["B2_ACCESS_KEY"]
    )
    bucket = b2_api.get_bucket_by_name(BUCKET_NAME)
else:
    logger.info("B2 environment variables not found. Disabling B2 uploads.")
    b2_authenticated = False


def file_exists(filename):
    url = f"https://f000.backblazeb2.com/file/{BUCKET_NAME}/{filename}"
    resp = httpx.head(url)
    return resp.status_code == httpx.codes.OK


# map of filenames to bytes
def upload(obj):
    if not b2_authenticated:
        logger.info("B2 not authenticated, bailing out of upload early.")
        return

    for filename, bytes in obj.items():
        if not file_exists(filename):
            bytes.seek(0)
            bucket.upload_bytes(bytes.read(), filename)
        else:
            logger.info(f"file {filename} already exists, skipping upload for it")
