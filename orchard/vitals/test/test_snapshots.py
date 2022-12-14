import pytest
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

PREFIX = "https://f000.backblazeb2.com/file/rdcodex"

@pytest.mark.parametrize(["url", "sha1"], [
    (f"{PREFIX}/know-you-2zRJRCjPqJx.rdzip", "f2ad0f76bbfedf96bec3451eb9ead014accb3047"),
    (f"{PREFIX}/rgb-7krFijAGF4D.rdzip", "88f48cdbd6a63773fcf44a38f5ed1ece00f399be"),
    (f"{PREFIX}/pull-EpgEYcGYPnU.rdzip", "bdbd0b30d6ea29f8a6d2e8602b8829508dcbfc02"),
    (f"{PREFIX}/swing-c2QGYcw8GLq.rdzip", "933bbbbd9c1d79a8c3d2946e5748548a414488ea"),
    (f"{PREFIX}/sol-e-ma-dVMtiNt856v.rdzip", "f909b918e876d72fe8c3d385ba03940f85b3b906"),
    (f"{PREFIX}/ennui-og-3VFE7LSmzSo.rdzip", "250da27a5bff4285dcbf22f13c9c287f7eaf30d7"),
    (f"{PREFIX}/one-forg-NqVywpSrZs1.rdzip", "a75d03f274c9032a6f75fa32ac57005615c04b47"),
    (f"{PREFIX}/one-uncu-eqSkB1ZX7Xz.rdzip", "1bf690214be382e78daa98a5c7e73b79a59cf610"),
    ("https://cdn.discordapp.com/attachments/439363565007142912/1040242016593920030/Samario_Making_A_Mistake_-_One_Uncued_Tresillo2.rdzip", "495bd9d1b759db53e600b3986df55bdf3a9c3653"),
    ("https://cdn.discordapp.com/attachments/439363565007142912/1040248915414503464/auburnsummer_-_Triplet_Testaaaaa1.rdzip", "460807d4b87deb9d94ab31369985ba96b5c95291"),
    (f"{PREFIX}/yi-xiao-Hg3afme47nr.rdzip", "82dfb357c88904400fbf7eebc2ff2d1820ad9f8f"),
    (f"{PREFIX}/banas-QbMoyaG2nfK.rdzip", "862f1ad3d2f6ae0580055700d79b8ae30c8771b2"),
    (f"{PREFIX}/jimmy-s-Ccby1RK3XJK.rdzip", "5bb2d7298237d15b44fbb0a9ca963c00ecb58866"),
])
def test_snapshot(snapshot, pt_download_file, url, sha1):
    with pt_download_file(url, sha1) as f:
        f.seek(0)
        actual = main(f)
        assert actual == snapshot(exclude=props(*EXCLUDE_FROM_SNAPSHOT))
