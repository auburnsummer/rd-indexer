from dotenv import load_dotenv

from orchard.utils.env import const_from_env, const_from_env_must

load_dotenv()

BOT_VERSION = "0.0.2"

BOT_TOKEN = const_from_env_must("BOT_TOKEN")
PUBLIC_KEY = const_from_env_must("PUBLIC_KEY")

# If specified, register guild-specific commands instead of global.
# this is because guild commands refresh instantly whereas global takes ~1 hr
DEV_GUILD = const_from_env_must("DEV_GUILD")
APPLICATION_ID = const_from_env_must("APPLICATION_ID")
PATHLAB_ROLE = const_from_env("PATHLAB_ROLE")

SECRET_KEY_ORCH = const_from_env("SECRET_KEY_ORCH")

TYPESENSE_URL = const_from_env("TYPESENSE_URL")
TYPESENSE_API_KEY = "nicolebestgirl"

POST_STATUS_DOT_DB_TOKEN = const_from_env("POST_STATUS_DOT_DB_TOKEN")

GITHUB_TOKEN = const_from_env("GITHUB_TOKEN")


class ComponentType:
    ACTION_ROW = 1
    BUTTON = 2


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


class ButtonStyle:
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


class PermissionType:
    ROLE = 1
    USER = 2


DEFAULT_DB_STATUS_VALUE = {"approval": 0}
