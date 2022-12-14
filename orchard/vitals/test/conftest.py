import contextlib
import glob
import httpx
import pytest
from pathlib import Path

from orchard.vitals.facets.sha1_facet import _sha1

# # resolve short names to full path names
# @pytest.fixture

TMP_CACHE_DIRECTORY = "/tmp/orchard-vitals"

@pytest.fixture
def pt_download_file():
    return _pt_download_file

@contextlib.contextmanager
def _pt_download_file(url, sha1):
    """
    Download a file or retrieve it from a shared cache.
    """
    cache_directory = Path(TMP_CACHE_DIRECTORY)
    cache_directory.mkdir(parents=True, exist_ok=True)
    # do we already have it?
    file_path = cache_directory / sha1
    try:
        with file_path.open("rb") as f:
            if _sha1(f) == sha1:
                yield f
                return
    except IOError:
        pass

    # if we're here it doesn't exist yet, or the sha1 is incorrect.
    with file_path.open("wb") as f:
        with httpx.stream("GET", url, timeout=httpx.Timeout(None)) as r:
            for data in r.iter_bytes():
                f.write(data)
    
    with file_path.open("rb") as f:
        if _sha1(f) == sha1:
            yield f
        else:
            # if we're here, it didn't match the sha1
            raise Exception(f"Downloaded file {url} did not match the stated sha hash.")

def rdzip_paths():
    path = Path(__file__).parent # / "./fixtures/*.rdzip"
    glob = list(path.glob("./fixtures/*.rdzip"))
    return glob

@pytest.fixture
def rdzip_path_map():
    return rdzip_path_map2()

def rdzip_path_map2():
    glob = rdzip_paths()
    return { p.name: p.as_posix() for p in glob }

# def pytest_generate_tests(metafunc):
#     if "rdzip" in metafunc.fixturenames:
#         # get all my rdzips
#         rdzip_map = rdzip_path_map2()
#         metafunc.parametrize("rdzip", list(rdzip_map.keys()))