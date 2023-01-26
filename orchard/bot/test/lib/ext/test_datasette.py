from orchard.bot.lib.ext.datasette import fill_in_params, datasette_request
from orchard.db.models import Level
import pytest

def test_fill_in_params():
    assert fill_in_params("SELECT * FROM ?", ["orchard"]) == "SELECT * FROM \"orchard\""

def test_fill_in_params_number():
    assert fill_in_params("SELECT * FROM orchard WHERE param = ?", [2]) == "SELECT * FROM orchard WHERE param = 2"

@pytest.mark.asyncio
async def test_datasette_request(empty_db, datasette_responses):
    Level.bind(empty_db)
    result = await datasette_request(Level.select().where(Level.artist == "auburnsummer"))
    for r in result:
        assert r.artist == "auburnsummer"

@pytest.mark.asyncio
async def test_datasette_request_empty(empty_db, datasette_responses):
    Level.bind(empty_db)
    result = await datasette_request(Level.select().where(Level.artist == "fjaiwpejpawjopfawefawe"))
    assert result == []