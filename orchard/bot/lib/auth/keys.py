
import functools
import json
import base64

from datetime import datetime, timedelta

from orchard.bot.lib.constants import SECRET_KEY_ORCH
from orchard.bot.lib.utils import OrchardJSONResponse

from cryptography.fernet import Fernet


def _get_fernet():
    f = Fernet(SECRET_KEY_ORCH)
    return f

# f = Fernet(SECRET_KEY_ORCH)

def gen_passcode():
    """
    Generate a passcode. they have an expiry of one week
    """
    f = _get_fernet()
    now = datetime.now()
    expr = now + timedelta(weeks=4)
    payload = {"version": 1, "exp": expr.isoformat()}
    message = json.dumps(payload).encode("utf-8")
    return f.encrypt(message).decode('utf-8')


def check_passcode(s):
    """
    Check if a passcode is valid. throws exception if not.
    """
    f = _get_fernet()
    plaintext = f.decrypt(s.encode('utf-8'))
    parsed = json.loads(plaintext)
    exp = datetime.fromisoformat(parsed["exp"])
    if exp < datetime.now():
        raise Exception("This passcode has expired")
    return True

def with_passcode(func):
    """
    A decorator. Adds token authentication to the handler.
    """
    @functools.wraps(func)
    async def inner(request):
        try:
            if "authorization" not in request.headers:
                raise ValueError("There should be an Authorization header, but there aint")
            token_type, token = request.headers["authorization"].split(" ")
            if token_type.lower() != "bearer":
                raise ValueError("Token type should be Bearer.")
            check_passcode(token)
        except Exception as e:
            return OrchardJSONResponse({"error": str(e)}, 401)
        else:
            return await func(request)
    
    return inner