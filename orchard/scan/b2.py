import logging
from dotenv import load_dotenv
import os
from b2sdk.v2 import *
from b2sdk import exception

logger = logging.getLogger(__name__)

load_dotenv()

BUCKET_NAME = "rdcodex"

if 'KEY_ID' in os.environ and 'B2_ACCESS_KEY' in os.environ:
    b2_authenticated = True
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    b2_api.authorize_account("production", os.environ['KEY_ID'], os.environ['B2_ACCESS_KEY'])
    bucket = b2_api.get_bucket_by_name(BUCKET_NAME)
else:
    logger.info("B2 environment variables not found. Disabling B2 uploads.")
    b2_authenticated = False

# map of filenames to bytes
def upload(obj):
    if not b2_authenticated:
        logger.info("B2 not authenticated, bailing out of upload early.")
        return
    
    for filename, bytes in obj.items():
        # check it's not already there.
        try:
            bucket.get_file_info_by_name(filename)
        except exception.FileNotPresent:
            # happy path is here actually
            bytes.seek(0)
            bucket.upload_bytes(bytes.read(), filename)
        else:
            logger.info(f"file {filename} already exists, skipping upload for it")


