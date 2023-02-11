from orchard.bot.lib.comm.message_builder import MessageBuilder
from orchard.bot.lib.constants import RoleMentionType
from datetime import datetime


def test_message_builder_simple_properties():
    m = MessageBuilder().content("Hello World")
    assert m.payload() == {"content": "Hello World"}


def test_message_builder_ephemereal():
    m = MessageBuilder().content("Hello World").ephemeral()
    assert m.payload() == {"content": "Hello World", "flags": 64}


def test_message_builder_a_subsequent_call_cancels_the_first():
    m = (
        MessageBuilder()
        .content("a")
        .content("b")
        .content("c")
        .ephemeral(True)
        .ephemeral(False)
    )
    assert m.payload() == {"content": "c", "flags": 0}


def test_message_builder_allowed_mentions():
    m = (
        MessageBuilder()
        .content("hello @everyone nice to meetcha")
        .start_allowed_mentions()
        .parse({RoleMentionType.EVERYONE})
        .done()
    )
    assert m.payload() == {
        "content": "hello @everyone nice to meetcha",
        "allowed_mentions": {"parse": ["everyone"]},
    }


def test_message_builder_some_embeds():
    m = (
        MessageBuilder()
        .start_embed()
        .title("This is an embed!")
        .description("Description of the first embed")
        .done()
        .start_embed()
        .title("The second embed")
        .description("Second embed....")
        .timestamp(datetime(year=1900, month=11, day=3))
        .footer("a footer at the bottom", "https://example.com")
        .field("hello", "yep")
        .field("hello2", "nope")
        .done()
    )
    assert m.payload() == {
        "embeds": [
            {
                "description": "Description of the first embed",
                "title": "This is an embed!",
            },
            {
                "description": "Second embed....",
                "fields": [
                    {"inline": False, "name": "hello", "value": "yep"},
                    {"inline": False, "name": "hello2", "value": "nope"},
                ],
                "footer": {
                    "icon_url": "https://example.com",
                    "text": "a footer at the bottom",
                },
                "timestamp": "1900-11-03T00:00:00",
                "title": "The second embed",
            },
        ],
    }


def test_message_builder_some_buttons():
    m = MessageBuilder().start_button().label("hello this is a button").done()
    assert m.payload() == {
        "components": [
            {
                "type": 1,
                "components": [
                    {"type": 2, "style": 1, "label": "hello this is a button"}
                ],
            }
        ]
    }


def test_message_builder_more_than_five_buttons_makes_new_row():
    m = MessageBuilder()
    for _ in range(6):
        m = m.start_button().label("Hello").done()
    assert m.payload() == {
        "components": [
            {
                "components": [
                    {"label": "Hello", "style": 1, "type": 2},
                    {"label": "Hello", "style": 1, "type": 2},
                    {"label": "Hello", "style": 1, "type": 2},
                    {"label": "Hello", "style": 1, "type": 2},
                    {"label": "Hello", "style": 1, "type": 2},
                ],
                "type": 1,
            },
            {"components": [{"label": "Hello", "style": 1, "type": 2}], "type": 1},
        ],
    }


def test_message_builder_force_new_row_makes_new_row():
    m = (
        MessageBuilder()
        .start_button()
        .label("First button")
        .done()
        .start_button(True)
        .label("Second button")
        .done()
    )
    assert m.payload() == {
        "components": [
            {
                "type": 1,
                "components": [{"type": 2, "style": 1, "label": "First button"}],
            },
            {
                "type": 1,
                "components": [{"type": 2, "style": 1, "label": "Second button"}],
            },
        ]
    }
