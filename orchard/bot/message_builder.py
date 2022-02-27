from orchard.bot.constants import ButtonStyle, ComponentType


class MessageBuilder:
    def __init__(self):
        self._dict = {"flags": 0}

    def content(self, content):
        self._dict["content"] = content
        return self

    # https://discord.com/developers/docs/interactions/receiving-and-responding#create-followup-message
    def ephemeral(self, yes=True):
        self._dict["flags"] = 64 if yes else 0
        return self

    def embed(self, embed):
        if "embeds" not in self._dict:
            self._dict["embeds"] = []

        self._dict["embeds"].append(embed.payload())
        return self

    def payload(self):
        print(self._dict)
        return self._dict

    def row(self, row: "ActionRow"):
        if "components" not in self._dict:
            self._dict["components"] = []
        self._dict["components"].append(row.payload())
        return self

    def clear_rows(self):
        self._dict["components"] = []
        return self


class Embed:
    def __init__(self):
        self._dict = {}

    def payload(self):
        return self._dict

    def title(self, title):
        self._dict["title"] = title
        return self

    def url(self, url):
        self._dict["url"] = url
        return self

    def image(self, url):
        self._dict["image"] = {"url": url}
        return self

    def description(self, description):
        self._dict["description"] = description
        return self

    def color(self, color):
        self._dict["color"] = color
        return self

    def field(self, name, value, inline=False):
        if "fields" not in self._dict:
            self._dict["fields"] = []

        self._dict["fields"].append({"name": name, "value": value, "inline": inline})
        return self


class ActionRow:
    def __init__(self, *components):
        self._components = components

    def payload(self):
        return {
            "type": ComponentType.ACTION_ROW,
            "components": [c.payload() for c in self._components],
        }


class Button:
    def __init__(
        self,
        style=ButtonStyle.PRIMARY,
        label=None,
        emoji=None,
        url=None,
        disabled=False,
        custom_id=None,
    ):
        # create a dictionary consisting only of the values given that were not None
        args = {
            "style": style,
            "label": label,
            "emoji": emoji,
            "url": url,
            "disabled": disabled,
            "custom_id": custom_id,
        }

        self._dict = {k: v for k, v in args.items() if v is not None}
        self._dict["type"] = ComponentType.BUTTON

    def payload(self):
        return self._dict
