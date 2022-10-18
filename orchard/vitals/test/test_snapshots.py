import pytest
from syrupy.extensions.single_file import SingleFileSnapshotExtension

from orchard.vitals.vitals import main
from syrupy.filters import props

# for vitals, we just test with snapshots.
# all levels used for snapshots are in the "fixtures" directory.

# snapshots don't necessarily show correctness of the data, just that it hasn't changed.
# so I have to remember to check the data added to the snapshot when I add new things to vitals.

EXCLUDE_FROM_SNAPSHOT = [
    "image",
    "thumb",
    "icon"
]


@pytest.fixture
def snapshot_ss(snapshot):
    return snapshot.use_extension(SingleFileSnapshotExtension)

def test_snapshot(rdzip, snapshot, rdzip_path_map):
    with open(rdzip_path_map[rdzip], "rb") as f:
        actual = main(f)
        assert actual == snapshot(exclude=props(*EXCLUDE_FROM_SNAPSHOT))

