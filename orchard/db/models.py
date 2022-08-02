from playhouse.sqlite_ext import JSONField
from peewee import *

# A level is a representation of the output of vitals.
# this is entirely deterministic based on the rdzip. there is no stateful data here.
class Level(Model):
    artist = TextField()
    artist_tokens = JSONField()
    authors = TextField()
    description = TextField()
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
    icon = TextField()
    id = TextField(primary_key=True)
    image = TextField()
    last_updated = DateTimeField()
    max_bpm = FloatField()
    min_bpm = FloatField()
    seizure_warning = BooleanField()
    sha1 = TextField()
    single_player = BooleanField()
    song = TextField()
    source = TextField()
    source_iid = TextField()
    tags = JSONField()
    thumb = TextField()
    two_player = BooleanField()
    url = TextField()
    url2 = TextField()

# a status is stateful data about a level.
# statuses map to levels. a level can have at most one status.
# however, a status can be 'free-floating', i.e. it does not point to a level that exists.
class Status(Model):
    id = TextField(primary_key=True)  # usually an FK to level
    approval = IntegerField()
    approval_reasons = TextField(null=True)
    indexed = DateTimeField(null=True)


