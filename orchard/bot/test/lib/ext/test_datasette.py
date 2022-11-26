from orchard.bot.lib.ext.datasette import fill_in_params, datasette_request
from orchard.db.models import Level
import pytest

def test_fill_in_params():
    assert fill_in_params("SELECT * FROM ?", ["orchard"]) == "SELECT * FROM \"orchard\""

def test_fill_in_params_number():
    assert fill_in_params("SELECT * FROM orchard WHERE param = ?", [2]) == "SELECT * FROM orchard WHERE param = 2"



@pytest.mark.asyncio
async def test_uhhhh(empty_db):
    Level.bind(empty_db)
    my_select = Level.select().where(Level.artist == "auburnsummer")
    raw_sql = fill_in_params(*my_select.sql())
    result = await datasette_request(raw_sql)
    print(result)
    print(result[0].authors)
    assert False
