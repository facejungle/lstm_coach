import json

from shared.utils.async_utils import instrumentsToCsv, request_async


class Bybit():
    def __init__(self):
        self.AppCfg: str = json.load(open('config.json', 'r'))
        self.BYBIT: str = self.AppCfg['markets']['bybit']
        self.fileInstruments: str = self.BYBIT['instruments']
        self.urlInstruments: str = self.BYBIT['url']['instruments']
        # self.urlCandles: str = self.BYBIT['url']['candles']

    async def parseInstruments(self, get=False):
        marketTypes = ['spot', 'linear']
        instruments = []
        markets = []
        for marketType in marketTypes:
            response = await request_async(self.urlInstruments + marketType)
            if get:
                return {'market:': marketType, "instruments": response['result']['list']}
            for inst in response['result']['list']:
                markets.append(marketType)
                instruments.append(inst['symbol'])
        await instrumentsToCsv(markets, instruments, self.fileInstruments)
