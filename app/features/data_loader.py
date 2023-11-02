"""class DataLoader"""
import importlib
import os
from pandas import DataFrame
from app.settings import Settings
from app.shared.data_processor import read_csv_async, write_csv_async
from app.shared.utils import new_thread, resource_path


class DataLoader():
    """class DataLoader"""

    def get_instruments_from_csv(self, exchange: str):
        """Async function for getting instruments from a csv file"""
        instruments_path = Settings().instruments_path + exchange + '.csv'
        instruments = new_thread(
            read_csv_async, [instruments_path], True)

        if instruments is not None and not instruments.empty:
            return instruments.sort_values(by="instrument")
        return None

    def get_volume_instruments(self, exchange) -> DataFrame | None:
        """Function for getting instruments """
        res_path = exchange
        instruments = new_thread(read_csv_async, [res_path], True)
        try:
            if not instruments.empty:
                instruments = instruments.sort_values(by="instrument")
                return instruments[instruments['market'] == 'SPOT'].values
        except AttributeError:
            return None
        return None

    def instruments_to_csv(self, instruments: DataFrame, filepath: str):
        """Import instruments to filepath"""
        res_path = resource_path(filepath)
        file = new_thread(read_csv_async, [res_path], True)

        if file is None or not file.equals(instruments):
            new_thread(write_csv_async, [instruments, res_path], True)
            print('Update: ', res_path)

    def get_exchanges_list(self):
        """Parse file names from app/shared/exchanges"""
        exchanges_path = Settings().exchanges_path
        return [name.split('.')[0] for name in os.listdir(exchanges_path) if name.endswith('.py') and name != "__init__.py"]  # pylint: disable=line-too-long

    def parse_save_instruments(self):
        """Async function for parse and save instruments to csv files"""
        exchanges = self.get_exchanges_list()
        classes_to_import = [{"module": "app.shared.exchanges." + exchange,
                              "class": exchange.capitalize()} for exchange in exchanges]

        for class_info in classes_to_import:
            module = importlib.import_module(class_info["module"])
            class_ = getattr(module, class_info["class"])
            instance = class_()
            instance.parse_instruments()
