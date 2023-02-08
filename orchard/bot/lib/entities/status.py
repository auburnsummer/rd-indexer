from datetime import datetime
from playhouse.shortcuts import model_to_dict

from orchard.bot.lib.constants import DEFAULT_DB_STATUS_VALUE
from orchard.bot.lib.entities.level import get_level
from orchard.db.models import Status


class StatusHelper:
    status: Status

    @classmethod
    async def create(cls, id: str):
        # check if the level exists. this throws if it doesn't.
        _ = await get_level(id)
        self = StatusHelper()
        self.status = _get_status(id)
        return self

    def set_approval(self, approval: int):
        s = self.status
        if approval >= 10 and s.approval < 10 and s.indexed is None:
            s.indexed = datetime.now()
        s.approval = approval
        s.save()

    def get(self):
        return self.status

    def to_dict(self):
        return model_to_dict(self.status)


def _get_status(id: str) -> Status:
    current, _ = Status.get_or_create(id=id, defaults=DEFAULT_DB_STATUS_VALUE)
    return current
