# https://stackoverflow.com/a/60758313

import peewee
from orchard.db.models import Status, User
from playhouse.shortcuts import model_to_dict

import logging

logger = logging.getLogger(__name__)


class UserHelper:
    user: User

    @classmethod
    def create(cls, id: str):
        self = UserHelper()
        self.user = _get_user(id)
        return self

    @classmethod
    def from_interaction(cls, body):
        id = body["member"]["user"]["id"]
        return cls.create(id)

    def get(self):
        return self.user

    def set_selected_level(self, level: Status):
        self.user.selected_level = level
        self.user.save()

    def to_dict(self):
        return model_to_dict(self.user)


def _get_user(id):
    try:
        return User.create(id=id, selected_level=None)
    except peewee.IntegrityError:
        return User.get(User.id == id)
