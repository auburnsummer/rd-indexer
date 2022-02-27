from zipfile import ZipFile
from slugify import slugify
from hashlib import blake2s
import base58

# id is a slug of the song + a cumulative hash of each internal file.
# this is so that identical zips that just have different metadata still resolve to the same id.

# the final hash is only 8 bytes long. we're not using this for security reasons.


def id_facet(obj, z: ZipFile):
    song = obj["settings"]["song"]

    hashes = []

    # for each file, get the blake2s hash
    for info in z.infolist():
        with z.open(info) as f:
            hash = blake2s(f.read())
            hashes.append(hash.hexdigest())

    # smush them together
    omnihash = "".join(sorted(hashes))

    # and has the result.
    omnihash2 = blake2s(omnihash.encode("utf-8"), digest_size=8)
    omnihash3 = base58.b58encode(omnihash2.digest()).decode("utf-8")

    return slugify(song, max_length=8) + "-" + omnihash3
