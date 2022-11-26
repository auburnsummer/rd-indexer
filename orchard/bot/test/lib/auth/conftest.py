import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from starlette.requests import Request
from starlette.responses import Response
from orchard.bot.lib.auth.discord_public_key import \
    with_discord_public_key_verification

from starlette.testclient import TestClient


@pytest.fixture
def disc_private_key(monkeypatch):
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw
    )

    monkeypatch.setattr("orchard.bot.lib.auth.discord_public_key.PUBLIC_KEY", public_bytes.hex())
    yield private_key

@pytest.fixture
def test_client():
    async def app(scope, receive, send):
        request = Request(scope, receive)

        @with_discord_public_key_verification
        async def inner(request):
            response = Response(status_code=204)
            return response

        resp = await inner(request)
        await resp(scope, receive, send)

    return TestClient(app)
