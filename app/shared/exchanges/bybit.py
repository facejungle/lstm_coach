from pandas import DataFrame
from app.features.data_loader import DataLoader
from app.shared.utils import new_thread, request_async, resource_path


class Bybit():
    def __init__(self):
        self.exchange_cfg: str = {
            "instruments": "data/instruments/bybit.csv",
            "candles": "data/candles/bybit/",
            "url": {
                "root": "https://api.bybit.com/v5/",
                "instruments": "https://api.bybit.com/v5/market/instruments-info?category=",
                "candles": ""
            }
        }

        self.file_instruments: str = resource_path(
            self.exchange_cfg['instruments'])
        self.url_instruments: str = self.exchange_cfg['url']['instruments']
        # self.urlCandles: str = self.BYBIT['url']['candles']

    def parse_instruments(self, get_results=False):
        market_types = ['spot', 'linear']
        data = []

        for market in market_types:
            response = new_thread(
                request_async, [self.url_instruments + market], True)
            for inst in response['result']['list']:
                data.append({"market": market, "instrument": inst['symbol']})

        results = DataFrame(data, columns=["market", "instrument"])

        if get_results:
            return results

        DataLoader().instruments_to_csv(results, self.file_instruments)
