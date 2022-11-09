import pytest
from playhouse.sqlite_ext import SqliteExtDatabase
from orchard.db.models import Level
from orchard.scan.sources.interface import RDLevelScraper
from unittest.mock import patch
from datetime import datetime
import os

@pytest.fixture
def patch_vitals():
    def fake_vitals(f):
        iid = f.read().decode('utf-8')
        return {
            "id": f"unittest_{iid}",
            "artist": "Joe",
            "artist_tokens": ["Joe"],
            "song": f"The Unit Test Song",
            "song_ct": {"len": 18, "color": "default"},
            "seizure_warning": False,
            "description": "",
            "description_ct": {},
            "hue": 0.0,
            "authors": ["unittest"],
            "max_bpm": 120,
            "min_bpm": 120,
            "difficulty": 2,
            "single_player": True,
            "two_player": False,
            "last_updated": datetime.fromtimestamp(0),
            "tags": ["1p", "unittest", "if you are seeing this in rhythm.cafe something has gone wrong"],
            "image": None,
            "thumb": None,
            "icon": None,
            "has_classics": True,
            "has_oneshots": True,
            "has_squareshots": False,
            "has_freezeshots": False,
            "has_freetimes": False,
            "has_holds": False,
            "has_skipshots": False,
            "has_window_dance": False,
            "sha1": "fejwoifjawpoefopjawopefpaowef",
            "rdlevel_sha1": "wepaofawpoejfpawejfpoawefaew"
        }
    with patch("orchard.scan.scan.analyze", wraps=fake_vitals) as mock_vitals:
        yield

@pytest.fixture
def make_mock_scraper():
    class MockLevelScraper(RDLevelScraper):
        def __init__(self, iids, enable_metadata):
            self.iids = iids
            self.enable_metadata = enable_metadata

        async def get_iids(self):
            return self.iids

        async def download_iid(self, iid):
            # for the mock, return the iid itself as bytes.
            return iid.encode('utf-8')

        async def get_url(self, iid):
            return f"this.is.a.mock.url.com/{iid}"       

        async def get_metadata(self, iid):
            if self.enable_metadata:
                return {
                    "first_letter": iid[0],
                    "last_letter": iid[-1]
                }
            return None
    
    return MockLevelScraper

@pytest.fixture
def empty_db():
    db = SqliteExtDatabase(":memory:")
    return db