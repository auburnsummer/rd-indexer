import pytest
import logging
from orchard.scan.scan import main
from orchard.db.models import Level
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_scan(empty_db, make_mock_scraper, caplog, patch_vitals):
    caplog.set_level(logging.INFO)
    sources = [
        [
            'mock',
            make_mock_scraper,
            {
                "iids": ["a", "b", "c", "d", "e"]
            }
        ]
    ]
    await main(empty_db, sources)
    # after, we expect 5 things in the db.
    ids = set(level.id for level in Level.select())
    assert ids == set(["unittest_a", "unittest_b", "unittest_c", "unittest_d", "unittest_e"])


@pytest.mark.asyncio
async def test_scan_removes_an_iid_if_the_source_no_longer_provides_it(empty_db, make_mock_scraper, caplog, patch_vitals):
    caplog.set_level(logging.INFO)
    sources = [
        [
            'mock',
            make_mock_scraper,
            {
                "iids": ["a", "b", "c", "d", "e"]
            }
        ]
    ]
    await main(empty_db, sources)
    # after, we expect 5 things in the db.
    ids = set(level.id for level in Level.select())
    assert ids == set(["unittest_a", "unittest_b", "unittest_c", "unittest_d", "unittest_e"])

    sources = [
        [
            'mock',
            make_mock_scraper,
            {
                "iids": ["a", "b", "c", "d"]  # no e!
            }
        ]
    ]
    await main(empty_db, sources)
    ids = set(level.id for level in Level.select())
    assert "unittest_e" not in ids
