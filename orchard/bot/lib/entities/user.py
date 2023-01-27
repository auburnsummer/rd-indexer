
# https://stackoverflow.com/a/60758313

from orchard.db.models import User

class UserHelper:
    user: User

    @classmethod
    def create(cls, id):
        self = UserHelper()
        self.user = _get_user(id)
        return self

    @classmethod
    def from_interaction(cls, body):
        return cls.create(body["member"]["user"]["id"])

    async def set_selected_level(self, level):
        self.user.selected_level = level
        self.user.save()



def _get_user(id):
    current, _ = User.get_or_create(
        id=id,
        selected_level=None
    )
    return current