import aiohttp


async def request_async(url: str):
    """Async request"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data
