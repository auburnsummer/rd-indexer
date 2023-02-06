from datetime import datetime, timedelta
import json
from orchard.bot.lib.auth.keys import check_passcode, gen_passcode, with_passcode
from orchard.bot.lib.auth import keys
from cryptography.fernet import Fernet, InvalidToken
import pytest
from unittest.mock import Mock, patch
from starlette.requests import Request
from starlette.responses import Response
from starlette.testclient import TestClient


def test_gen_passcode(fake_key):
    passcode = gen_passcode()
    assert check_passcode(passcode) is True


def test_gen_passcode_wrong(fake_key):
    key = Fernet.generate_key()
    f = Fernet(key)
    now = datetime.now()
    expr = now + timedelta(weeks=4)
    payload = {"version": 1, "exp": expr.isoformat()}
    message = json.dumps(payload).encode("utf-8")
    passcode = f.encrypt(message).decode("utf-8")
    with pytest.raises(InvalidToken):
        check_passcode(passcode)


def test_gen_passcode_expired(fake_key):
    passcode = gen_passcode()

    # go 4 weeks into the future
    _now = datetime.now()

    def fake_datetime():
        return _now + timedelta(weeks=4)

    with patch(
        "orchard.bot.lib.auth.keys.datetime.now", wraps=fake_datetime
    ) as mock_datetime:
        with pytest.raises(Exception) as e_info:
            check_passcode(passcode)
        assert e_info.match("expired")


def test_with_passcode(test_client2):
    passcode = gen_passcode()

    resp = test_client2.post("/", headers={"Authorization": f"Bearer {passcode}"})
    assert resp.status_code == 204


def test_with_passcode_negative(test_client2):
    passcode = "helloworld"

    resp = test_client2.post("/", headers={"Authorization": f"Bearer {passcode}"})
    assert resp.status_code == 401


def test_with_passcode_no_header(test_client2):
    resp = test_client2.post("/")
    assert resp.status_code == 401
