from orchard.bot.lib.constants import ButtonStyle, ComponentType, RoleMentionType
from typing import Dict, Set, Optional
from datetime import datetime
from orchard.bot.lib.comm.pager import PagerUUID


class AllowedMentions:
    """
    A MessageBuilder component that handles the "allowed_mentions" field.
    https://discord.com/developers/docs/resources/channel#allowed-mentions-object
    """

    _back: "MessageBuilder"

    def __init__(self, mb: "MessageBuilder"):
        self._back = mb
        self._dict = {}

    def parse(self, allowed: Set[RoleMentionType]):
        self._dict["parse"] = [x.value for x in allowed]
        return self

    def users(self, allowed: Set[str]):
        self._dict["users"] = list(allowed)
        return self

    def roles(self, allowed: Set[str]):
        self._dict["roles"] = list(allowed)
        return self

    def replied_user(self, yes=True):
        self._dict["replied_user"] = yes
        return self

    def payload(self):
        return self._dict

    def done(self):
        "Move back into the MessageBuilder context."
        return self._back.allowed_mentions_direct(self)


class MessageEmbed:
    """
    A MessageBuilder component that handles an "embed" field.
    https://discord.com/developers/docs/resources/channel#embed-object
    """

    _back: "MessageBuilder"

    def __init__(self, mb: "MessageBuilder"):
        self._back = mb
        self._dict = {}

    def title(self, title: str):
        self._dict["title"] = title
        return self

    def description(self, description: str):
        self._dict["description"] = description
        return self

    def url(self, url: str):
        self._dict["url"] = url
        return self

    def timestamp(self, timestamp: datetime):
        self._dict["timestamp"] = timestamp.isoformat()
        return self

    def color(self, color: int):
        "suggest use of hex string here, e.g. 0xaabbcc"
        self._dict["color"] = color

    def footer(self, text: Optional[str] = None, icon_url: Optional[str] = None):
        new_footer = {}
        if text:
            new_footer["text"] = text
        if icon_url:
            new_footer["icon_url"] = icon_url
        self._dict["footer"] = new_footer
        return self

    def author(self, name: Optional[str] = None, icon_url: Optional[str] = None):
        new_author = {}
        if name:
            new_author["name"] = name
        if icon_url:
            new_author["icon_url"] = icon_url
        self._dict["author"] = new_author
        return self

    def image(self, url):
        self._dict["image"] = {"url": url}
        return self

    def field(self, name: str, value: str, inline=False):
        if "fields" not in self._dict:
            self._dict["fields"] = []

        self._dict["fields"].append({"name": name, "value": value, "inline": inline})
        return self

    def payload(self):
        return self._dict

    def done(self):
        return self._back.embed_direct(self)


class ActionButton:
    """
    Defines a button https://discord.com/developers/docs/interactions/message-components#buttons
    """

    _dict: Dict

    def __init__(self, mb: "MessageBuilder", force_new_row: bool):
        self._dict = {
            "type": ComponentType.BUTTON.value,
            "style": ButtonStyle.PRIMARY.value,
        }
        self._back = mb
        self._force_new_row = force_new_row  # not part of the payload, but read by MessageBuilder when deciding where to place this button.

    def style(self, style: ButtonStyle):
        self._dict["style"] = style.value
        return self

    def label(self, label: str):
        self._dict["label"] = label
        return self

    def emoji(self):
        pass  # not implemented yet.
        return self

    def uuid(self, uuid: PagerUUID):
        self._dict["custom_id"] = uuid
        return self

    def url(self, url: str):
        self._dict["url"] = url
        return self

    def disabled(self, yes=True):
        self._dict["disabled"] = yes

    def payload(self):
        return self._dict

    def done(self):
        return self._back.component_direct(self)


class MessageBuilder:
    """
    Builds a message object suitable for use with Interactor.post or Interactor.edit

    https://discord.com/developers/docs/interactions/receiving-and-responding#create-followup-message
    """

    def __init__(self):
        self._dict = {}

    def content(self, content: str):
        self._dict["content"] = content
        return self

    def ephemeral(self, yes=True):
        self._dict["flags"] = 64 if yes else 0
        return self

    def tts(self, yes=True):
        self._dict["tts"] = yes

    def allowed_mentions_direct(self, am: AllowedMentions):
        self._dict["allowed_mentions"] = am.payload()
        return self

    def start_allowed_mentions(self):
        "Set the allowed_mentions field. This moves into an AllowedMentions context. Use done() to move back to the MessageBuilder."
        am = AllowedMentions(self)
        return am

    def embed_direct(self, e: MessageEmbed):
        if "embeds" not in self._dict:
            self._dict["embeds"] = []

        self._dict["embeds"].append(e.payload())
        return self

    def start_embed(self):
        "Set an embed field. This moves into a MessageEmbed context. Use done() to move back to the MessageBuilder."
        e = MessageEmbed(self)
        return e

    def start_button(self, force_new_row=False):
        "Start an ActionButton context. Set force_new_row to always put it on a new row, otherwise it will try to fit it in the current row whenever possible."
        ab = ActionButton(self, force_new_row)
        return ab

    def component_direct(self, com: ActionButton):
        if "components" not in self._dict:
            self._dict["components"] = []

        components = self._dict["components"]
        need_new_row = False
        payload = com.payload()

        if com._force_new_row:
            need_new_row = True
        elif len(components) == 0:
            need_new_row = True
        elif payload["type"] == ComponentType.BUTTON.value:
            row = components[-1]["components"]
            # 5 or more buttons in the row.
            if (
                sum(
                    1
                    for component in row
                    if component["type"] == ComponentType.BUTTON.value
                )
                >= 5
            ):
                need_new_row = True
            # any select menu.
            selects = {
                ComponentType.CHANNEL_SELECT.value,
                ComponentType.MENTIONABLE_SELECT.value,
                ComponentType.ROLE_SELECT.value,
                ComponentType.STRING_SELECT.value,
                ComponentType.USER_SELECT.value,
            }
            if any(component["type"] in selects for component in row):
                need_new_row = True

        if need_new_row:
            new_row = {"type": ComponentType.ACTION_ROW.value, "components": []}
            components.append(new_row)

        row = components[-1]
        row["components"].append(payload)
        return self

    def clear_rows(self):
        if "components" in self._dict:
            del self._dict["components"]
        return self

    def payload(self):
        return self._dict


def start_message():
    """
    The usual entry point for creating a MessageBuilder, this one has sane defaults for things.
    """
    return (
        MessageBuilder()
        .start_allowed_mentions()
        .parse(set([]))  # by default a message cannot ping anyone.
        .done()
    )
