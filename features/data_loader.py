import asyncio
from shared.exchanges.binance import Binance
from shared.exchanges.bybit import Bybit
from shared.exchanges.okx import Okx


class DataLoader():
    def __init__(self):
        self.Binance = Binance()
        self.Bybit = Bybit()
        self.Okx = Okx()

    async def getInstruments(self):
        task1 = asyncio.create_task(coro=self.Binance.parseInstruments())
        task2 = asyncio.create_task(coro=self.Bybit.parseInstruments())
        task3 = asyncio.create_task(coro=self.Okx.parseInstruments())
        await asyncio.gather(task1, task2, task3)
