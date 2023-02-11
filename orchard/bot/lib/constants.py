from dotenv import load_dotenv

from orchard.utils.env import const_from_env

from enum import Enum

load_dotenv()

BOT_VERSION = const_from_env("BOT_VERSION", "dev")

PUBLIC_KEY = const_from_env("PUBLIC_KEY")
BOT_TOKEN = const_from_env("BOT_TOKEN")

DEV_GUILD = const_from_env("DEV_GUILD")
APPLICATION_ID = const_from_env("APPLICATION_ID")

SECRET_KEY_ORCH = const_from_env("SECRET_KEY_ORCH")

TYPESENSE_URL = const_from_env("TYPESENSE_URL")
TYPESENSE_API_KEY = "nicolebestgirl"

GITHUB_TOKEN = const_from_env("GITHUB_TOKEN")

LITESTREAM_ON = const_from_env("LITESTREAM_ON") == "true"


class RoleMentionType(Enum):
    ROLE = "roles"
    USER = "users"
    EVERYONE = "everyone"


class ComponentType(Enum):
    ACTION_ROW = 1
    BUTTON = 2
    STRING_SELECT = 3
    TEXT_INPUT = 4
    USER_SELECT = 5
    ROLE_SELECT = 6
    MENTIONABLE_SELECT = 7
    CHANNEL_SELECT = 8


class OptionType:
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9


class ResponseType:
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE = 7


class ButtonStyle(Enum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


class PermissionType:
    ROLE = 1
    USER = 2


DEFAULT_DB_STATUS_VALUE = {"approval": 0}
