from sqlite_utils import Database
import sys

# create an aggregate table combining level and status
def make_aggregate(db):
    db.execute("CREATE TABLE levels AS SELECT * FROM level LEFT JOIN status ON level.id = status.id")

def add_indexes(db):
    indexes = {
        "levels" : [
            "difficulty",
            "seizure_warning",
            "last_updated",
            "single_player",
            "two_player",
            "has_classics",
            "has_oneshots",
            "has_squareshots",
            "has_swing",
            "has_freetimes",
            "has_holds",
            "uploaded",
            "approval",
            "kudos"
        ]
    }
    for table, collist in indexes.items():
        for col in collist:
            db[table].create_index([col], if_not_exists=True)

def enable_fts(db):
    cols = [
        "artist",
        "song",
        "description",
        "tags",
        "authors"
    ]
    db["levels"].enable_fts(cols, create_triggers=True)
    db["levels"].optimize()

def enable_counts(db):
    db.enable_counts()

def vac(db):
    db.vacuum()


if __name__ == "__main__":
    db = Database(sys.argv[1])
    for f in [make_aggregate, add_indexes, enable_fts, enable_counts, vac]:
        f(db)
