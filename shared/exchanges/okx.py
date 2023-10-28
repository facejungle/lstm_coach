import json

from shared.utils.async_utils import instrumentsToCsv, request_async


class Okx():
    def __init__(self):
        self.AppCfg: str = json.load(open('config.json', 'r'))
        self.OKX: str = self.AppCfg['markets']['okx']
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
        await instrumentsToCsv(markets, instruments, self.fileInstruments)
