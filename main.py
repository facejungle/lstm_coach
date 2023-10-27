from app.service import Service
from features.data_loader import DataLoader
import asyncio


async def main():
    if __name__ == '__main__':
        app = Service()
        test = DataLoader()

        await test.getInstruments()
        await app.start()
asyncio.run(main())
