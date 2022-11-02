from datetime import datetime

from orchard.bot.constants import DEFAULT_DB_STATUS_VALUE
from orchard.db.models import Status

def get_status(id):
    current, _ = Status.get_or_create(
        id=id,
        defaults=DEFAULT_DB_STATUS_VALUE
    )
    return current

def set_status(id, value):
    current = get_status(id)
    # update indexed if this is newly approved.
    if "approval" in value and value["approval"] >= 10 and current.approval < 10 and current.indexed is None:
        value["indexed"] = datetime.now()

    q = Status.update(**value).where(Status.id == id)
    q.execute()