from orchard.scan.sources.interface import RDLevelScraper
import requests

SHEET_API_URL = "https://script.google.com/macros/s/AKfycbzm3I9ENulE7uOmze53cyDuj7Igi7fmGiQ6w045fCRxs_sK3D4/exec"


class OldSheetScraper(RDLevelScraper):
    def __init__(self):
        pass

    async def get_iids(self):
        r = requests.get(SHEET_API_URL)
        return [l["download_url"] for l in r.json()]

    async def download_iid(self, iid):
        return requests.get(iid).content

    async def get_url(self, iid):
        return iid
