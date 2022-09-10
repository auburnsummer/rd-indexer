import glob
from pathlib import Path

def pytest_generate_tests(metafunc):
    if "rdzip" in metafunc.fixturenames:
        # get all my rdzips
        path = Path(__file__).parent / "./fixtures/*.rdzip"
        rdzips = glob.glob(path.absolute().as_posix())
        metafunc.parametrize("rdzip", rdzips)
