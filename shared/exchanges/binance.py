import asyncio
import json

from shared.utils.async_utils import instrumentsToCsv, request_async


class Binance():
    def __init__(self):
        self.AppCfg: str = json.load(open('config.json', 'r'))
        self.BINANCE: str = self.AppCfg['markets']['binance']
        self.fileInstruments: str = self.BINANCE['instruments']
        self.urlInstruments: str = self.BINANCE['url']['instruments']
        self.urlCandles: str = self.BINANCE['url']['candles']

    async def parseInstruments(self, get=False):
        response = await request_async(self.urlInstruments)
        markets = []
        instruments = []
        for inst in response['symbols']:
            for market in inst['permissions']:
                if market == 'SPOT' or market == 'MARGIN' or market == 'LEVERAGED':
                    markets.append(market)
                    instruments.append(inst['symbol'])
        await instrumentsToCsv(markets, instruments, self.fileInstruments)
        if get:
            return response

    async def parseCandles(self, instrument: str, timeframe: str, qty: int = None, start_time: int = None):
        results: list = await request_async(self.BINANCE['url']['candles'] + instrument + '&interval=' + timeframe)

        if qty:
            while len(results) < qty:
                url = self.BINANCE['url']['candles'] + instrument + \
                    '&interval=' + timeframe + \
                    '&endTime=' + str(results[-1][0]) + '&limit=500'
                results.extend(await request_async(url))
                print(len(results))
