import json
import pandas as pd
import asyncio

from shared.utils.async_utils import request_async, read_csv, write_csv


class DataLoader():
    def __init__(self):
        self.AppCfg: str = json.load(open('config.json', 'r'))
        self.BINANCE: str = self.AppCfg['markets']['binance']
        self.OKX: str = self.AppCfg['markets']['okx']
        self.BYBIT: str = self.AppCfg['markets']['bybit']

    async def getInstruments(self):
        await asyncio.gather(self.parseBinanceInstruments(), self.parseOkxInstruments(), self.parseBybitInstruments())

    async def parseBinanceInstruments(self, get=False):
        response = await request_async(self.BINANCE['url']['instruments'])
        markets = []
        instruments = []
        for inst in response['symbols']:
            for market in inst['permissions']:
                if market == 'SPOT' or market == 'MARGIN' or market == 'LEVERAGED':
                    markets.append(market)
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
            response = await asyncio.gather(request_async(self.OKX['url']['instruments'] + marketType))
            if get:
                return {'market:': marketType, "data": response['data']}
            for inst in response[0]['data']:
                markets.append(inst['instType'])
                instruments.append(inst['instId'])
        await self.instrumentsToCsv(markets, instruments, self.OKX['instruments'])

    async def parseBybitInstruments(self, get=False):
        marketTypes = ['spot', 'linear']
        instruments = []
        markets = []
        for marketType in marketTypes:
            response = await asyncio.gather(request_async(self.BYBIT['url']['instruments'] + marketType))
            if get:
                return {'market:': marketType, "instruments": response['result']['list']}
            for inst in response[0]['result']['list']:
                markets.append(marketType)
                instruments.append(inst['symbol'])
        await self.instrumentsToCsv(markets, instruments, self.BYBIT['instruments'])

    async def instrumentsToCsv(self, markets: list, instruments: list, filepath: str):
        file = await read_csv(filepath)
        df = pd.DataFrame({"market": markets, "instrument": instruments})
        if not file.equals(df):
            await write_csv(df, filepath)
            print('Update: ', filepath)
