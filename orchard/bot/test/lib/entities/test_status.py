
from unittest.mock import patch
from orchard.db.models import Status
from datetime import datetime, timedelta


# def test_get_status_with_existing_thing(empty_db_with_status_bind):
#     Status.create(id="test_id", approval=5)
#     assert get_status("test_id").approval == 5

# def test_get_status_with_non_existing_id_creates_default(empty_db_with_status_bind):
#     assert get_status("does_not_exist").approval == 0

# def test_set_status_sets_the_approval(empty_db_with_status_bind):
#     set_status("test_id", {"approval": 20})
#     assert get_status("test_id").approval == 20

# def test_set_status_updates_indexed_if_newly_approved(empty_db_with_status_bind):
#     Status.create(id="test_id", approval=5)
#     assert get_status("test_id").indexed is None

#     _now = datetime.now()
#     with patch("orchard.bot.lib.auth.keys.datetime.now", wraps=lambda: _now) as mock_datetime:
#         set_status("test_id", {"approval": 10})
#         assert get_status("test_id").indexed == _now

# def test_set_status_does_not_update_indexed_if_not_approved(empty_db_with_status_bind):
#     Status.create(id="test_id", approval=5)
#     assert get_status("test_id").indexed is None
#     set_status("test_id", {"approval": 9})
#     assert get_status("test_id").indexed is None

# def test_set_status_does_not_update_indexed_if_indexed_already_set(empty_db_with_status_bind):
#     time = datetime.now() - timedelta(days=2)
#     Status.create(id="test_id", approval=5, indexed=time)
#     set_status("test_id", {"approval": 10})
#     assert get_status("test_id").indexed == time


