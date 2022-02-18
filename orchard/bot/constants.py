from dotenv import load_dotenv

load_dotenv()
import os
from pathlib import Path

BOT_TOKEN = os.environ["BOT_TOKEN"]
PUBLIC_KEY = os.environ["PUBLIC_KEY"]
DISCORD_API_URL = "https://discord.com/api/v8"

# If specified, register guild-specific commands instead of global.
# this is because guild commands refresh instantly whereas global takes ~1 hr
DEV_GUILD = os.environ["DEV_GUILD"] if "DEV_GUILD" in os.environ else False
APPLICATION_ID = os.environ["APPLICATION_ID"]
PATHLAB_ROLE = os.environ["PATHLAB_ROLE"]

SECRET_KEY_ORCH = bytes.fromhex(os.environ["SECRET_KEY_ORCH"])

DB_PATH = Path.cwd() / "orchard.db"
DB_URL = "https://f000.backblazeb2.com/file/rhythm-cafe/orchard-main.db"

ORCHARD_API_URL = "https://api.rhythm.cafe/orchard.json"

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