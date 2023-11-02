"""Binance exchange class"""
from pandas import DataFrame
from app.features.data_loader import DataLoader
from app.shared.utils import new_thread, request_async, resource_path


class Binance():
    """Binance exchange class"""

    def __init__(self):
        self.exchange_cfg: str = {
            "instruments": "data/instruments/binance.csv",
            "candles": "data/candles/binance/",
            "url": {
                "root": "https://api.binance.com/api/v3/",
                "instruments": "https://api.binance.com/api/v3/exchangeInfo",
                "candles": "https://api.binance.com/api/v3/klines?symbol="
            }
        }
        self.file_instruments: str = resource_path(
            self.exchange_cfg['instruments'])
        self.url_instruments: str = self.exchange_cfg['url']['instruments']
        self.url_candles: str = self.exchange_cfg['url']['candles']

    def parse_instruments(self, get_response=False):
        """Binance exchange class"""
        response = new_thread(request_async, [self.url_instruments], True)
        data = []

        for inst in response['symbols']:
            for market in inst['permissions']:
                if market in ('SPOT', 'MARGIN', 'LEVERAGED'):
                    data.append(
                        {"market": market, "instrument": inst['symbol']})

        results = DataFrame(data, columns=["market", "instrument"])
        DataLoader().instruments_to_csv(results, self.file_instruments)

        if get_response:
            return response

        self.parse_candles('BTCUSDC', '1d', 1000)

    def parse_candles(self, instrument: str, timeframe: str, qty: int = None):
        """Binance exchange class"""
        results: list = new_thread(request_async, [
            self.exchange_cfg['url']['candles'] + instrument + '&interval=' + timeframe], True)

        if qty:
            while len(results) < qty:
                url = self.exchange_cfg['url']['candles'] + instrument + \
                    '&interval=' + timeframe + \
                    '&endTime=' + str(results[-1][0]) + '&limit=500'
                results.extend(new_thread(request_async, [url], True))
                print(len(results))
        return results
