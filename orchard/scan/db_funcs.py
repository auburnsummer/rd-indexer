from orchard.db.models import Level


def add_level(level):
    Level.create(**level)


def delete_level(source_id, source_iid):
    Level.delete().where((Level.source == source_id) & (Level.source_iid == source_iid)).execute()


def level_exists( id):
    return Level.get_or_none(Level.id == id) is not None


def get_source_set(source_id):
    return set(row.source_iid for row in Level.select().where(Level.source == source_id))
