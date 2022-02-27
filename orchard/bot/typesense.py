import httpx

from orchard.bot.constants import TYPESENSE_URL, TYPESENSE_API_KEY

AUTH_HEADERS = {
    'x-typesense-api-key': TYPESENSE_API_KEY
}

async def get_by_id(id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{TYPESENSE_URL}/collections/levels/documents/{id}", headers=AUTH_HEADERS)
        resp.raise_for_status()
        return resp.json()