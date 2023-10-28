import io
import pandas as pd

import aiofiles
import aiohttp


async def request_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data


async def read_csv(file_path):
    async with aiofiles.open(file_path, mode='r') as file:
        content = await file.read()
        if content.strip():
            df = pd.read_csv(io.StringIO(content))
            return df
        else:
            return pd.DataFrame()


async def write_csv(data, file_path):
    async with aiofiles.open(file_path, mode='w') as file:
        async with aiofiles.open(file_path, mode='w') as file:
            csv_content = data.to_csv(index=False)
            await file.write(csv_content)


async def instrumentsToCsv(markets: list, instruments: list, filepath: str):
    file = await read_csv(filepath)
    df = pd.DataFrame({"market": markets, "instrument": instruments})
    if not file.equals(df):
        await write_csv(df, filepath)
        print('Update: ', filepath)
