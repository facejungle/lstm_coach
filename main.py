"""
RNN LSTM AI Coach application
"""
import asyncio
from app.service import Service

if __name__ == '__main__':
    asyncio.run(Service().start())
