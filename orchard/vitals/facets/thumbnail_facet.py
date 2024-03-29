from math import ceil
from zipfile import ZipFile
from PIL import Image

from io import BytesIO

from orchard.vitals.arguments_decorator import with_arguments

THUMBNAIL_WIDTH = 300
THUMBNAIL_HEIGHT = 168


@with_arguments("obj", "zip")
def thumbnail_facet(obj, z: ZipFile):
    """return two file objects, one for the thumbnail and the original."""
    image_name = obj["settings"]["previewImage"]

    orig_file_p = BytesIO()
    thumb_file_p = BytesIO()
    with z.open(image_name, "r") as image_buffer:
        image = Image.open(image_buffer)
        orig = image.copy()
        image.thumbnail((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), Image.Resampling.LANCZOS)

        orig.save(orig_file_p, format="png")
        image.save(thumb_file_p, format="png")

    return orig_file_p, thumb_file_p
