from orchard.vitals.vitals import main


def test_haha_awesome(rdzip, snapshot):
    with open(rdzip, "rb") as f:
        assert main(f) == snapshot
    assert True