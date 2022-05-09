from abc import ABC, abstractmethod


class RDLevelScraper(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    # return a list of level iids. each id should map 1:1 to a level.
    @abstractmethod
    async def get_iids(self):
        pass

    # return the contents of the rdzip of an iid, as bytes.
    @abstractmethod
    async def download_iid(self, iid):
        pass

    # if an external (non-codex) URL is available for this iid, return it, or None otherwise.
    @abstractmethod
    async def get_url(self, iid):
        pass

    # optional callback function that gets called whenever orchard indexes a level from this source.
    # Note that on_index receives a full level object
    async def on_index(self, level):
        pass

    # ditto for deletions.
    # Note that on_delete receives only an iid. this is because the level has already been deleted
    async def on_delete(self, iid):
        pass
