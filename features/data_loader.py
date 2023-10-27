import io
import json
import aiofiles
import aiohttp
import pandas as pd
import asyncio


class DataLoader():
    def __init__(self):
        self.AppCfg: str = json.load(open('config.json', 'r'))
        self.BINANCE: str = self.AppCfg['markets']['binance']
        self.OKX: str = self.AppCfg['markets']['okx']
        self.BYBIT: str = self.AppCfg['markets']['bybit']

    async def make_request(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                return data

    async def read_csv_async(self, file_path):
        async with aiofiles.open(file_path, mode='r') as file:
            content = await file.read()
            if content.strip():
                df = pd.read_csv(io.StringIO(content))
                return df
            else:
                return pd.DataFrame()

    async def write_csv_async(self, data, file_path):
        async with aiofiles.open(file_path, mode='w') as file:
            async with aiofiles.open(file_path, mode='w') as file:
                csv_content = data.to_csv(index=False)
                await file.write(csv_content)

    async def getInstruments(self):
        await asyncio.gather(self.parseBinanceInstruments(), self.parseOkxInstruments())

    async def parseBinanceInstruments(self, get=False):
        response = await self.make_request(self.BINANCE['url']['instruments'])
        markets = []
        instruments = []
        for inst in response['symbols']:
            for market in inst['permissions']:
                if market == 'SPOT' or market == 'MARGIN':
                    markets.append(market)
                    instruments.append(inst['symbol'])
                elif market == 'LEVERAGED':
                    markets.append('SWAP')
                    instruments.append(inst['symbol'])
        await self.instrumentsToCsv(markets, instruments,
                                    self.BINANCE['instruments'])
        if get:
            return response

    async def parseOkxInstruments(self, get=False):
        marketTypes = ['SPOT', 'SWAP', 'MARGIN']
        instruments = []
        markets = []
        for marketType in marketTypes:
            response = await asyncio.gather(self.make_request(self.OKX['url']['instruments'] + marketType))
            if get:
                return {'market:': marketType, "data": response['data']}
            for inst in response[0]['data']:
                markets.append(inst['instType'])
                instruments.append(inst['instId'])
        await self.instrumentsToCsv(markets, instruments, self.OKX['instruments'])

    async def instrumentsToCsv(self, markets: list, instruments: list, filepath: str):
        file = await self.read_csv_async(filepath)
        df = pd.DataFrame({"market": markets, "instrument": instruments})
        print(file)
        if not file.equals(df):
            await self.write_csv_async(df, filepath)
            print('Update inst')
        else:
            print('dont update inst')
