import asyncio
import logging

import httpx

logger = logging.getLogger(__name__)

def wrapper(fn):
    """
    wrap httpx's methods to handle discord rate limits.
    """
    async def inner(*args, **kwargs):
        resp: httpx.Response = await fn(*args, **kwargs)
        while resp.status_code == 429:
            # retry
            time_to_wait = float(resp.headers['x-ratelimit-reset-after']) + 0.1
            print(f"We are being rate limited! Waiting {time_to_wait} seconds...")
            await asyncio.sleep(time_to_wait)
            resp = await fn(*args, **kwargs)

        resp.raise_for_status()

        # wait a little longer, perhaps
        try:
            if float(resp.headers['x-ratelimit-remaining']) < 1:
                additional_wait_time = float(resp.headers['x-ratelimit-reset-after'])
                logger.info(f"A ratelimit is imminent! waiting {additional_wait_time} seconds to avoid it...")
                await asyncio.sleep(additional_wait_time)
        except KeyError:
            # discord might not give us these. 
            pass
        return resp

    return inner


class Client:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.get = wrapper(self.client.get)
        self.post = wrapper(self.client.post)
        self.put = wrapper(self.client.put)
        self.delete = wrapper(self.client.delete)
        self.head = wrapper(self.client.head)
        self.options = wrapper(self.client.options)
        self.patch = wrapper(self.client.patch)
        self.send = wrapper(self.client.send)
        self.aclose = self.client.aclose

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.client.aclose()