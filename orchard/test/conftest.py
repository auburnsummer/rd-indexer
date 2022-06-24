import glob


def pytest_generate_tests(metafunc):
    print("hi")
    if "rdzip" in metafunc.fixturenames:
        # get all my rdzips
        rdzip_paths = glob.glob("./fixtures/*.rdzip")
        metafunc.parametrize("rdzip", rdzip_paths)
