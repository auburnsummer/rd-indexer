# parse a unity-style <color> string
# returns a tuple of the string _without_ the colors, then what bits are colored by 0-indexed ranges.
import re


class InvalidColorException(Exception):
    pass

# (<color=([a-zA-Z0-9#]+)>)|(<\/color>)
# TAG_FINDER = re.compile(r'(<color=(["a-zA-Z0-9#]+)>)|(<\/color>)')

TAG_FINDER2 = re.compile(r'<\/?color.*?>')

def parse_color_tagged_string(s: str):
    stripped = re.sub(TAG_FINDER2, "", s.strip())

    dummy_token = [
        {"len": len(stripped), "color": "default"}
    ]

    return stripped, dummy_token