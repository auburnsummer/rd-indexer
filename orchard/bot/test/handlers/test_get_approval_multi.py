from datetime import datetime
import pytest
from orchard.bot.handlers.get_approval_multi import get_approval_multi

from orchard.db.models import Status
from starlette.requests import Request
from starlette.testclient import TestClient
from starlette.applications import Starlette
from starlette.routing import Route

@pytest.fixture
def test_client():
    app = Starlette(routes=[Route("/", get_approval_multi.__wrapped__, methods=["POST"])])
    tc = TestClient(app)
    return tc

@pytest.mark.asyncio
async def test_get_approval_multi(empty_db_with_status_bind, test_client):
    # seed data
    Status.bulk_create([
        Status(id="a", approval=0),
        Status(id="b", approval=0),
        Status(id="c", approval=10, indexed=datetime.fromtimestamp(1669895626))
    ])

    
    resp = test_client.post("/", json=["a", "b", "c"])
    resp.raise_for_status()
    assert resp.status_code == 200
    assert resp.json() == [
        {'approval': 0,
        'approval_reasons': None,
        'id': 'a',
        'indexed': None},
        {'approval': 0,
        'approval_reasons': None,
        'id': 'b',
        'indexed': None},
        {'approval': 10,
        'approval_reasons': None,   'id': 'c',
        'indexed': '2022-12-01 11:53:46'},
 ]

@pytest.mark.asyncio
async def test_get_approval_doesnt_already_exist(empty_db_with_status_bind, test_client):
    resp = test_client.post("/", json=["a", "b", "c"])
    assert resp.status_code == 200
    assert resp.json() == [
        {'approval': 0,
        'approval_reasons': None,
        'id': 'a',
        'indexed': None},
        {'approval': 0,
        'approval_reasons': None,
        'id': 'b',
        'indexed': None},
        {'approval': 0,
        'approval_reasons': None,   'id': 'c',
        'indexed': None},
 ]



