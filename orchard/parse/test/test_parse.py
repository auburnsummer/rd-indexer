from orchard.parse import parse


def test_scalar_1():
    s = """
        {"value": 2}
    """
    assert parse(s) == {"value": 2}


def test_scalar_2():
    s = """
        {"value": "hello world"}
    """
    assert parse(s) == {"value": "hello world"}


def test_scalar_3():
    s = """
        {"value": false}
    """
    assert parse(s) == {"value": False}


def test_array_1():
    s = """
        [2, 4, 3, 5, 1]
    """
    assert parse(s) == [2, 4, 3, 5, 1]


def test_array_2():
    s = """
        [3,
        4,
        5,
        1,
        "hello world",
        {"a": 4},
        ]
    """
    assert parse(s) == [3, 4, 5, 1, "hello world", {"a": 4}]


def test_obj_1():
    s = """
        {
            "a": "hello",
            "b": "world",
            "c": "today",
            "d": {
                "e": "nesting now",
                "f": {
                    "g": "even further",
                    "h": [
                        "i", "j", "k"
                    ],
                }
            },
        },


    """
    assert parse(s) == {
        "a": "hello",
        "b": "world",
        "c": "today",
        "d": {
            "e": "nesting now",
            "f": {
                "g": "even further",
                "h": ["i", "j", "k"]
            }
        }
    }


def test_encoded_newlines():
    s = r"""
        {
            "a": "hello\nworld\nyep"
        }
    """
    assert parse(s) == {"a": "hello\nworld\nyep"}


def test_literal_newlines():
    s = r"""
        {
            "a": "this is a valid value
in an rdlevel even though
it has literal newlines!"
        }
    """
    assert parse(s) == {"a": "this is a valid value\nin an rdlevel even though\nit has literal newlines!"}