from orchard.utils.env import const_from_env


def test_const_from_env(monkeypatch):
    monkeypatch.setenv("TEST_ENV", "HELLO_WORLD")
    assert const_from_env("TEST_ENV") == "HELLO_WORLD"


def test_const_from_env_default_when_not_defined(monkeypatch):
    monkeypatch.delenv("TEST_ENV", raising=False)
    assert const_from_env("TEST_ENV", "DEFAULT VALUE") == "DEFAULT VALUE"
