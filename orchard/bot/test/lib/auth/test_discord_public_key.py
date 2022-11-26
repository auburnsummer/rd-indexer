from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from time import time

def test_with_discord_public_key_verification_happy_path(disc_private_key, test_client):
    timestamp = str(int(time()))
    payload = b"Hello World"
    to_encrypt = timestamp.encode('ascii') + payload
    signature = disc_private_key.sign(to_encrypt)

    response = test_client.post('/', data=payload, headers={
        "x-signature-ed25519": signature.hex(),
        "x-signature-timestamp": timestamp
    })
    assert response.status_code == 204


def test_with_discord_public_key_verification_incorrect_payload(disc_private_key, test_client):
    timestamp = str(int(time()))
    payload = b"Hello World"
    to_encrypt = timestamp.encode('ascii') + payload + b"extra data after"
    signature = disc_private_key.sign(to_encrypt)

    response = test_client.post('/', data=payload, headers={
        "x-signature-ed25519": signature.hex(),
        "x-signature-timestamp": timestamp
    })
    assert response.status_code == 401

def test_with_discord_public_key_verification_incorrect_signature(disc_private_key, test_client):
    different_private_key = Ed25519PrivateKey.generate()
    timestamp = str(int(time()))
    payload = b"Hello World"
    to_encrypt = timestamp.encode('ascii') + payload
    signature = different_private_key.sign(to_encrypt)

    response = test_client.post('/', data=payload, headers={
        "x-signature-ed25519": signature.hex(),
        "x-signature-timestamp": timestamp
    })
    assert response.status_code == 401