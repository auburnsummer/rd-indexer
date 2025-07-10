# this is the md5 hash of the .rdlevel file based on the author/artist/song fields
# which should be identical to what RD uses to save custom level scores. 
import hashlib

from orchard.vitals.arguments_decorator import with_arguments

@with_arguments("obj")
def rdlevel_md5_facet(obj):
    md5 = hashlib.md5()
    author = obj["settings"]["author"]
    artist = obj["settings"]["artist"]
    song = obj["settings"]["song"]

    md5.update(author.encode("utf-8"))
    md5.update(artist.encode("utf-8"))
    md5.update(song.encode("utf-8"))

    return md5.hexdigest()