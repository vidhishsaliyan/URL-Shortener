import httpx
async def is_url_reachable(url: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.head(url=url, timeout=5)
            print(response)
            return response.status_code < 400
    except:
        return False
