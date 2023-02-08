import pytest
from starlette.requests import Request
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.testclient import TestClient

from orchard.bot.handlers.set_approval import set_approval
from orchard.db.models import Status
from unittest.mock import patch


@pytest.fixture
def test_client():
    app = Starlette(
        routes=[Route("/{id}", set_approval.__wrapped__, methods=["GET", "POST"])]
    )
    tc = TestClient(app)
    return tc


def test_set_approval_works_with_get(
    empty_db_with_status_bind, patch_get_level, test_client
):
    Status.bulk_create([Status(id="a", approval=15)])
    resp = test_client.get("/a")
    resp.raise_for_status()
    assert resp.status_code == 200
    assert resp.json() == {
        "id": "a",
        "approval": 15,
        "indexed": None,
        "approval_reasons": None,
    }


def test_set_approval_works_with_post(
    empty_db_with_status_bind, patch_get_level, test_client
):
    Status.bulk_create([Status(id="a", approval=15)])
    resp = test_client.post("/a", json={"approval": 25})
    assert resp.status_code == 200
    assert resp.json()["approval"] == 25
    assert Status.get_by_id("a").approval == 25
