import json
from features.async_utils import request_async
from features.data_processor import instruments_to_csv
from features.utils import resource_path


class Okx():
    def __init__(self):
        self.AppCfg: str = json.load(
            open(resource_path('shared\\exchanges\\config.json'), 'r', encoding='utf-8'))
        self.OKX: str = self.AppCfg['okx']
        self.fileInstruments: str = self.OKX['instruments']
        self.urlInstruments: str = self.OKX['url']['instruments']

    async def parseInstruments(self, get=False):
        marketTypes = ['SPOT', 'SWAP', 'MARGIN']
        instruments = []
        markets = []
        for marketType in marketTypes:
            response = await request_async(self.urlInstruments + marketType)
            if get:
                return {'market:': marketType, "data": response['data']}
            for inst in response['data']:
                markets.append(inst['instType'])
                instruments.append(inst['instId'])
        instruments_to_csv(markets, instruments, self.fileInstruments)
