"""
RNN LSTM AI Coach application
"""
import asyncio
from app.service import app_loader

if __name__ == '__main__':
    asyncio.run(app_loader())
