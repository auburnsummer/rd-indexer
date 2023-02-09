import json
import pathlib
import pytest
from orchard.db.models import Level

curr = pathlib.Path(__file__).parent / "fixtures"

# map of URLs to a json file in the fixtures subdirectory with the contents of the request.
# these are generally generated just using curl: curl "url" > 1.json
# and then copy paste the URL you put into here.
SAVED_RESPONSES = {
    "https://api.rhythm.cafe/datasette/orchard.json?sql=SELECT+%22t1%22.%22id%22%2C+%22t1%22.%22artist%22%2C+%22t1%22.%22artist_tokens%22%2C+%22t1%22.%22authors%22%2C+%22t1%22.%22description%22%2C+%22t1%22.%22description_ct%22%2C+%22t1%22.%22difficulty%22%2C+%22t1%22.%22has_classics%22%2C+%22t1%22.%22has_freetimes%22%2C+%22t1%22.%22has_freezeshots%22%2C+%22t1%22.%22has_holds%22%2C+%22t1%22.%22has_oneshots%22%2C+%22t1%22.%22has_skipshots%22%2C+%22t1%22.%22has_squareshots%22%2C+%22t1%22.%22has_window_dance%22%2C+%22t1%22.%22hue%22%2C+%22t1%22.%22icon%22%2C+%22t1%22.%22image%22%2C+%22t1%22.%22last_updated%22%2C+%22t1%22.%22max_bpm%22%2C+%22t1%22.%22min_bpm%22%2C+%22t1%22.%22rdlevel_sha1%22%2C+%22t1%22.%22seizure_warning%22%2C+%22t1%22.%22sha1%22%2C+%22t1%22.%22single_player%22%2C+%22t1%22.%22song%22%2C+%22t1%22.%22song_ct%22%2C+%22t1%22.%22source%22%2C+%22t1%22.%22source_iid%22%2C+%22t1%22.%22source_metadata%22%2C+%22t1%22.%22tags%22%2C+%22t1%22.%22thumb%22%2C+%22t1%22.%22two_player%22%2C+%22t1%22.%22url%22%2C+%22t1%22.%22url2%22+FROM+%22level%22+AS+%22t1%22+WHERE+%28%22t1%22.%22artist%22+%3D+%22auburnsummer%22%29&_json=artist_tokens&_json=authors&_json=description_ct&_json=song_ct&_json=source_metadata&_json=tags": curr
    / "1.json",
    "https://api.rhythm.cafe/datasette/orchard.json?sql=SELECT+%22t1%22.%22id%22%2C+%22t1%22.%22artist%22%2C+%22t1%22.%22artist_tokens%22%2C+%22t1%22.%22authors%22%2C+%22t1%22.%22description%22%2C+%22t1%22.%22description_ct%22%2C+%22t1%22.%22difficulty%22%2C+%22t1%22.%22has_classics%22%2C+%22t1%22.%22has_freetimes%22%2C+%22t1%22.%22has_freezeshots%22%2C+%22t1%22.%22has_holds%22%2C+%22t1%22.%22has_oneshots%22%2C+%22t1%22.%22has_skipshots%22%2C+%22t1%22.%22has_squareshots%22%2C+%22t1%22.%22has_window_dance%22%2C+%22t1%22.%22hue%22%2C+%22t1%22.%22icon%22%2C+%22t1%22.%22image%22%2C+%22t1%22.%22last_updated%22%2C+%22t1%22.%22max_bpm%22%2C+%22t1%22.%22min_bpm%22%2C+%22t1%22.%22rdlevel_sha1%22%2C+%22t1%22.%22seizure_warning%22%2C+%22t1%22.%22sha1%22%2C+%22t1%22.%22single_player%22%2C+%22t1%22.%22song%22%2C+%22t1%22.%22song_ct%22%2C+%22t1%22.%22source%22%2C+%22t1%22.%22source_iid%22%2C+%22t1%22.%22source_metadata%22%2C+%22t1%22.%22tags%22%2C+%22t1%22.%22thumb%22%2C+%22t1%22.%22two_player%22%2C+%22t1%22.%22url%22%2C+%22t1%22.%22url2%22+FROM+%22level%22+AS+%22t1%22+WHERE+%28%22t1%22.%22artist%22+%3D+%22fjaiwpejpawjopfawefawe%22%29&_json=artist_tokens&_json=authors&_json=description_ct&_json=song_ct&_json=source_metadata&_json=tags": curr
    / "2.json",
}


@pytest.fixture
def datasette_responses(httpx_mock):
    for key, value in SAVED_RESPONSES.items():
        with value.open("r") as f:
            contents = json.loads(f.read())
            httpx_mock.add_response(url=key, json=contents)


@pytest.fixture
def empty_db_with_level(empty_db):
    Level.bind(empty_db)
    empty_db.create_tables([Level])
    return empty_db
