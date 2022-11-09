
import json
import base64

from datetime import datetime, timedelta

from orchard.bot.lib.constants import SECRET_KEY_ORCH

from cryptography.fernet import Fernet

f = Fernet(SECRET_KEY_ORCH)


def gen_passcode():
    """
    Generate a passcode. they have an expiry of one week
    """
    now = datetime.now()
    expr = now + timedelta(weeks=4)
    payload = {"version": 1, "exp": expr.isoformat()}
    message = json.dumps(payload).encode("utf-8")
    return f.encrypt(message).decode('utf-8')


def check_passcode(s):
    """
    Check if a passcode is valid. throws exception if not.
    """
    plaintext = f.decrypt(s.encode('utf-8'))
    parsed = json.loads(plaintext)
    exp = datetime.fromisoformat(parsed["exp"])
    if exp < datetime.now():
        raise Exception("This passcode has expired")
    return True
