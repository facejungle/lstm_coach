import asyncio
from features.utils import new_thread
from shared.exchanges import okx, binance, bybit


class Exchanges():
    def __init__(self) -> None:
        self.binance = binance.Binance()
        self.bybit = bybit.Bybit()
        self.okx = okx.Okx()

    def parse_save_instruments_wrapper(self):
        """Function wrapper for parse and save instruments to csv files"""
        new_thread(self.parse_save_instruments, f_async=True)

    async def parse_save_instruments(self):
        """Async function for parse and save instruments to csv files"""
        task1 = asyncio.create_task(coro=self.binance.parseInstruments())
        task2 = asyncio.create_task(coro=self.bybit.parseInstruments())
        task3 = asyncio.create_task(coro=self.okx.parseInstruments())
        await asyncio.gather(task1, task2, task3)
