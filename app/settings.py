from app.shared.utils import resource_path


class Settings():
    def __init__(self) -> None:
        self.exchanges_path = resource_path('app/shared/exchanges/')
        self.instruments_path = resource_path('data/instruments/')
        self.candles_path = resource_path('data/candles/')
