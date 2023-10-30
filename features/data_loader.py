"""class DataLoader"""
import json
from pandas import DataFrame
from features.data_processor import read_csv_async
from features.utils import new_thread, resource_path


class DataLoader():
    """class DataLoader"""

    def __init__(self):
        exchange_cfg_path = resource_path('shared\\exchanges\\config.json')
        self.exchange_cfg = json.load(
            open(exchange_cfg_path, 'r', encoding='utf-8'))

    def get_volume_instruments(self) -> DataFrame | None:
        """Function for getting instruments """
        inst_path = resource_path(self.exchange_cfg['binance']['instruments'])
        instruments = new_thread(read_csv_async, ([inst_path, True]), True)
        try:
            if not instruments.empty:
                instruments = instruments.sort_values(by="instrument")
                return instruments[instruments['market'] == 'SPOT'].values
        except AttributeError:
            return None
        return None


def get_instrument_files():
    2
