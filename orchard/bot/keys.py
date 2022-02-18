import nacl.secret
import nacl.utils
import json
import base64

from datetime import datetime, timedelta

from orchard.bot.constants import SECRET_KEY_ORCH

box = nacl.secret.SecretBox(SECRET_KEY_ORCH)

def gen_passcode():
    """
    Generate a passcode. they have an expiry of one week    
    """
    now = datetime.now()
    expr = now + timedelta(weeks=1)
    payload = {
        'version': 1,
        'exp': expr.isoformat()
    }
    message = json.dumps(payload).encode('utf-8')
    encrypted = box.encrypt(message)
    return base64.b64encode(encrypted).decode('utf-8')


# 1B8UZ/rtWkR3ycgKjPRrhi4jqv5e0Qn3ixPk/SuFn9orlr2TmzDE7aDLCVSr+gNKahtxWzKHWH429V0hpwpuAtDJ1jlqS4p6czg2CzLdy7YQPYufBe1oZ9sNow==

def check_passcode(s):
    """
    Check if a passcode is valid. throws exception if not.
    """
    decoded_bytes = base64.b64decode(s)
    plaintext = box.decrypt(decoded_bytes)
    parsed = json.loads(plaintext)
    exp = datetime.fromisoformat(parsed['exp'])
    if exp < datetime.now():
        raise Exception("This passcode has expired")
    return True
