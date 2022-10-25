import functools
import json

from playhouse.sqlite_ext import JSONField
from peewee import *

my_json_dumps = functools.partial(json.dumps, ensure_ascii=False)
MyJsonField = functools.partial(JSONField, json_dumps=my_json_dumps)

# A level is a representation of the output of vitals.
# this is entirely deterministic based on the rdzip. there is no stateful data here.
# NOTE TO SELF: changes here must be reflected in Combined below.

class Level(Model):
    artist = TextField()
    artist_tokens = MyJsonField()
    authors = MyJsonField()
    description = TextField()
    description_ct = MyJsonField()
    difficulty = IntegerField()
    has_classics = BooleanField()
    has_freetimes = BooleanField()
    has_freezeshots = BooleanField()
    has_holds = BooleanField()
    has_oneshots = BooleanField()
    has_skipshots = BooleanField()
    has_squareshots = BooleanField()
    has_window_dance = BooleanField()
    hue = FloatField()
    icon = TextField(null=True)
    id = TextField(primary_key=True)
    image = TextField()
    last_updated = DateTimeField()
    max_bpm = FloatField()
    min_bpm = FloatField()
    rdlevel_sha1 = TextField()
    seizure_warning = BooleanField()
    sha1 = TextField()
    single_player = BooleanField()
    song = TextField()
    song_ct = MyJsonField()
    source = TextField()
    source_iid = TextField()
    source_metadata = MyJsonField(null=True)
    tags = MyJsonField()
    thumb = TextField(null=True)
    two_player = BooleanField()
    url = TextField(null=True)
    url2 = TextField()


# a status is stateful data about a level.
# statuses map to levels. a level can have at most one status.
# however, a status can be 'free-floating', i.e. it does not point to a level that exists.
# NOTE TO SELF: changes here must be reflected in Combined below.
class Status(Model):
    id = TextField(primary_key=True)  # usually an FK to level
    approval = IntegerField()
    approval_reasons = TextField(null=True)
    indexed = DateTimeField(null=True)


# the combined model combines a Level and Status.'
# this is only used for the Datasette representation in package.py.

class Combined(Model):
    artist = TextField()
    artist_tokens = MyJsonField()
    authors = MyJsonField()
    description = TextField()
    description_ct = MyJsonField()
    difficulty = IntegerField()
    has_classics = BooleanField()
    has_freetimes = BooleanField()
    has_freezeshots = BooleanField()
    has_holds = BooleanField()
    has_oneshots = BooleanField()
    has_skipshots = BooleanField()
    has_squareshots = BooleanField()
    has_window_dance = BooleanField()
    hue = FloatField()
    icon = TextField(null=True)
    id = TextField(primary_key=True)
    image = TextField()
    last_updated = DateTimeField()
    max_bpm = FloatField()
    min_bpm = FloatField()
    rdlevel_sha1 = TextField()
    seizure_warning = BooleanField()
    sha1 = TextField()
    single_player = BooleanField()
    song = TextField()
    song_ct = MyJsonField()
    source = TextField()
    source_iid = TextField()
    source_metadata = MyJsonField(null=True)
    tags = MyJsonField()
    thumb = TextField(null=True)
    two_player = BooleanField()
    url = TextField(null=True)
    url2 = TextField()
    # STATUS
    approval = IntegerField()
    approval_reasons = TextField(null=True)
    indexed = DateTimeField(null=True)

