from orchard.db.models import Level
import httpx

# async def datasette_request(s):
#     with httpx.AsyncClient() as client:
#         r = await client.get("https://api.rhythm.cafe/datasette/orchard.json", params={"sql": s})
#         json = 




# def test_level_query_ds(empty_db):
#     Level.bind(empty_db)
#     my_select = Level.select().where(Level.has_classics == True)
#     raw_sql = fill_in_params(*my_select.sql())
#     print(raw_sql)
#     assert False    
