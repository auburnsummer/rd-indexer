from zipfile import ZipFile
from PIL import Image

from io import BytesIO

from orchard.vitals.arguments_decorator import with_arguments


@with_arguments("obj", "zip")
def icon_facet(obj, z: ZipFile):
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
