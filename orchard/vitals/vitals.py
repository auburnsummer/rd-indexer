import sys
import zipfile
from typing import BinaryIO
from orchard.parse import parse
from orchard.vitals.facets.author_facet import author_facet
from orchard.vitals.facets.beat_types_facet import beat_type_facet
from orchard.vitals.facets.bpm_facet import bpm_facet
from orchard.vitals.facets.difficulty_facet import difficulty_facet
from orchard.vitals.facets.icon_facet import icon_facet
from orchard.vitals.facets.id_facet import id_facet
from orchard.vitals.facets.key_facet import make_key_facet
from orchard.vitals.facets.player_facet import player_facet
from orchard.vitals.facets.tags_facet import tags_facet
from orchard.vitals.facets.thumbnail_facet import thumbnail_facet
from orchard.vitals.facets.updated_facet import updated_facet


class VitalsException(Exception):
    pass


def main(f: BinaryIO):
    facets = {
        "id":                               id_facet,
        "artist":                           make_key_facet(["settings", "artist"]),
        "song":                             make_key_facet(["settings", "song"]),
        "seizure_warning":                  make_key_facet(["settings", "seizureWarning"], True),
        "description":                      make_key_facet(["settings", "description"]),
        "hue":                              make_key_facet(["settings", "songNameHue"], 0.0),
        "authors":                          author_facet,
        ("max_bpm", "min_bpm"):             bpm_facet,
        "difficulty":                       difficulty_facet,
        ("single_player", "two_player"):    player_facet,
        "last_updated":                     updated_facet,
        "tags":                             tags_facet,
        ("image", "thumb"):                 thumbnail_facet,
        "icon":                             icon_facet,
        (
            "has_classics",
            "has_oneshots",
            "has_squareshots",
            "has_freezeshots",
            "has_freetimes",
            "has_holds"
        ):                                  beat_type_facet
    }

    try:
        with zipfile.ZipFile(f) as z:
            with z.open('main.rdlevel', 'r') as rdlevel:
                text = rdlevel.read().decode('utf-8-sig')
                parsed = parse(text)

                final = {}
                for key, func in facets.items():
                    try:
                        result = func(parsed, z)
                        if isinstance(key, tuple):
                            # multiple keys with (expected) multiple values that map to the keys.
                            for k, v in zip(key, result):
                                final[k] = v
                        else:
                            final[key] = result
                    except Exception as e:
                        raise VitalsException(f"vitals: An unhandled error occured in a facet: {e}")

                return final

    except zipfile.BadZipFile:
        raise VitalsException("vitals: this is not a zip file, or we couldn't decode it for some reason.")
    except KeyError:
        raise VitalsException("vitals: there is no main.rdlevel in the zip.")

if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
        with open(file_name, 'rb') as f:
            vit = main(f)
    except IndexError:
        print("Did you pass a file name in?")