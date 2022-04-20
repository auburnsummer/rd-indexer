from math import ceil
from zipfile import ZipFile
from PIL import Image

from io import BytesIO

THUMBNAIL_WIDTH = 300
THUMBNAIL_HEIGHT = 168

# return two fake file objects, one for the thumbnail and the original.
def icon_facet(obj, z: ZipFile, _):
    try:
        image_name = obj["settings"]["syringeIcon"]
    except:
        return None

    if not image_name:
        return None

    file_p = BytesIO()
    try:
        with z.open(image_name, "r") as image_buffer:
            image = Image.open(image_buffer)
            image.save(file_p, format="png")

        return file_p
    except:
        # icon is allowed to be None
        return None
