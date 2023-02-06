import pytest


@pytest.fixture
def dig_obj():
    obj = {
        "hello": {"world": {"hi": 2, "bye": 3, "ummmmm": 4}},
        "hello2": {"world": [2, 4, 3, 5, "bbbbbbb"]},
    }
    return obj
