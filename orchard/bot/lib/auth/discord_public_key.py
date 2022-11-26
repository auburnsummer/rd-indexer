from collections import defaultdict
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
from starlette.responses import JSONResponse
from orchard.bot.lib.constants import PUBLIC_KEY


def with_discord_public_key_verification(func):
    """
    A decorator. Wrap a starlette handler to check discord's auth beforehand
    https://discord.com/developers/docs/interactions/slash-commands#security-and-authorization
    """
    async def inner(request):
        verify_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(PUBLIC_KEY))
        rheaders = defaultdict(str, request.headers)
        signature = rheaders["x-signature-ed25519"]
        timestamp = rheaders["x-signature-timestamp"]
        payload = await request.body()
        # concat bytes together
        to_verify = timestamp.encode('ascii') + payload

        try:
            verify_key.verify(bytes.fromhex(signature), to_verify)
        except InvalidSignature:
            return JSONResponse({"error": "Invalid request signature"}, status_code=401)
        
        return await func(request)

    return inner

