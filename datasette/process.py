from sqlite_utils import Database
import sys

def add_indexes(db):
    indexes = {
        "level" : [
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
            "has_holds"
        ],
        "status": [
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
    db["level"].enable_fts(cols, create_triggers=True)
    db["level"].optimize()

def enable_counts(db):
    db.enable_counts()

def vac(db):
    db.vacuum()

def add_levels_view(db):
    db.create_view("levels", "select * from level left join status ON level.id = status.id", replace=True)


if __name__ == "__main__":
    db = Database(sys.argv[1])
    for f in [add_levels_view, add_indexes, enable_fts, enable_counts, vac]:
        f(db)
