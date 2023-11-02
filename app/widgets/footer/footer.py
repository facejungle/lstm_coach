from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import mplfinance as mpf
import pandas as pd
from app.features.model import AiModel
from app.shared.exchanges.binance import Binance

from app.style import APP_STYLE


def make_app_footer(self):
    self.footer_frame = ttk.Frame(
        self.main_view,
        height=50
    )
    self.footer_frame.pack(fill="x", side="bottom")

    def step():
        # progress['value'] += 20
        progress.start(1)
    progress = ttk.Progressbar(
        self.footer_frame, orient="horizontal", length=APP_STYLE['window']['min_w'] / 2, mode='determinate')
    progress.pack(side="right")
    # fig = Figure()

    # ax = fig.add_subplot(111)
    datas = Binance().parse_candles('BTCUSDC', '1h')
    data = pd.DataFrame(datas, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                        'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data['open'] = pd.to_numeric(data['open'])
    data['high'] = pd.to_numeric(data['high'])
    data['low'] = pd.to_numeric(data['low'])
    data['close'] = pd.to_numeric(data['close'])
    data['volume'] = pd.to_numeric(data['volume'])
    data.set_index('timestamp', inplace=True)

    mc = mpf.make_marketcolors(up='g', down='r', inherit=True)
    s = mpf.make_mpf_style(marketcolors=mc)
    mpf.plot(data, type='candle', style=s, volume=True)
    # canvas = FigureCanvasTkAgg(fig, master=self.footer_frame)
    # canvas.draw()
    # canvas.get_tk_widget().pack()
    config = {
        "data": [data[4] for data in datas],
        "x_train_length": 10,
        "y_train_length": 5,
        "deep_training": 100,
        "layers": [
            {
                "type": "lstm",
                "params": {
                    "units": 123,
                    "input_shape": (234,),
                    "dropout": 0.2
                }
            },
            {
                "type": "dense",
                "params": {
                    "units": 123
                }
            }
        ],
        "optimizer": 'adam',
        "loss": 'mean_squared_error',
        "epochs": 10,
        "batch_size": 32
    }
    model = AiModel(config)
    model.build_model()
    model.compile_model()
    history = model.start_training()
    print(history)
