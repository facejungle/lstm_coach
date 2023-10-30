import json
from features.async_utils import request_async
from features.data_processor import instruments_to_csv
from features.utils import resource_path


class Bybit():
    def __init__(self):
        self.AppCfg: str = json.load(
            open(resource_path('shared\\exchanges\\config.json'), 'r', encoding='utf-8'))
        self.BYBIT: str = self.AppCfg['bybit']
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
        instruments_to_csv(markets, instruments, self.fileInstruments)
