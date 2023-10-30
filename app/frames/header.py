"""Module providing a function to print the Python version."""
import asyncio
import json
from time import sleep
from tkinter import BOTH, CENTER, TOP, X, Frame, StringVar, ttk
from app.style.style import app_styles
from features.data_loader import DataLoader
from features.data_processor import read_csv_thread
from features.utils import resource_path, new_thread


def make_app_header(self):
    """Module providing a function to print the Python version."""
    self.header_frame = Frame(
        self.main_view
    )
    self.header_frame.pack(fill=X, side=TOP)
    make_first_line(self)
    make_second_line(self)


def make_first_line(self):
    """Make first line on header for app."""
    first_line_frame = Frame(self.header_frame)
    first_line_frame.pack(
        fill="x",
        side="top"
    )

# EXCHANGE FRAME
    exchange_frame = Frame(first_line_frame)
    exchange_frame.pack(
        anchor="w",
        side="left",
        padx=app_styles['pad_x'],
        pady=app_styles['pad_y'],
    )
    exchange_label = ttk.Label(
        exchange_frame,
        text="Exchange",
        background="#ccc",
    )
    exchange_label.pack(side="top", anchor="n", fill="x")
    exchange_cfg_path = resource_path('shared\\exchanges\\config.json')
    exchange_cfg = json.load(open(exchange_cfg_path, 'r', encoding='utf-8'))
    exchanges = list(exchange_cfg)
    exchange_var = StringVar(value=exchanges[0])

    def choice_exchange(event):
        exchange_selection = exchange_field.get()
        market_field.set('')
        instruments_field.set('')
        if exchange_selection in exchanges:
            inst_path = resource_path(
                exchange_cfg[exchange_selection]['instruments'])
            instruments = read_csv_thread(
                inst_path).sort_values(by="instrument")
            exchange_markets = instruments['market'].unique()
            market_field.configure(
                values=list(exchange_markets))

    def choice_market(event):
        market_selection = market_field.get()
        instruments_field.set('')
        exchange_selection = exchange_field.get()
        if exchange_selection in exchanges:
            inst_path = resource_path(
                exchange_cfg[exchange_selection]['instruments'])
            instruments = read_csv_thread(
                inst_path).sort_values(by="instrument")
            exchange_instruments = instruments[instruments['market']
                                               == market_selection].values
            instruments_field.configure(
                values=[inst[1] for inst in exchange_instruments])
    exchange_field = ttk.Combobox(
        exchange_frame,
        values=exchanges,
        textvariable=exchange_var,
        height=5,
        state='readonly'
    )
    exchange_field.pack(side='bottom', anchor="s")
    exchange_field.bind("<<ComboboxSelected>>", choice_exchange)

# MARKETS FRAME
    market_frame = Frame(first_line_frame)
    market_frame.pack(
        anchor="w",
        side="left",
        padx=app_styles['pad_x'],
        pady=app_styles['pad_y'],
    )
    market_label = ttk.Label(
        market_frame,
        text="Market",
        background="#ccc",
    )
    market_label.pack(side="top", anchor="n", fill="x")
    market_field = ttk.Combobox(
        market_frame,
        height=5,
        state='readonly'
    )
    market_field.pack(side='bottom', anchor="s")
    market_field.bind("<<ComboboxSelected>>", choice_market)

# INSTRUMENTS FRAME
    instruments_frame = Frame(first_line_frame)
    instruments_frame.pack(
        anchor="w",
        side="left",
        padx=app_styles['pad_x'],
        pady=app_styles['pad_y'],
    )
    instruments_label = ttk.Label(
        instruments_frame,
        text="Instruments",
        background="#ccc"
    )
    instruments_label.pack(side="top", anchor="n", fill="x")
    instruments_field = ttk.Combobox(
        instruments_frame,
        height=5,
        state='readonly'
    )
    instruments_field.pack(side='bottom', anchor="s")

# VOLUME FRAME
    volume_frame = Frame(first_line_frame)
    volume_frame.pack(
        anchor="w",
        side="left",
        padx=app_styles['pad_x'],
        pady=app_styles['pad_y'],
    )
    volume_label = ttk.Label(
        volume_frame,
        text="Volume",
        background="#ccc"
    )
    volume_label.pack(side="top", anchor="n", fill="x")
    volume_field = ttk.Combobox(
        volume_frame,
        values=exchanges,
        height=5,
        state='readonly'
    )
    volume_field.pack(side='bottom', anchor="s")
    volume_instruments = new_thread(
        DataLoader().get_volume_instruments)

    volume_field.configure(values=[inst[1]
                                   for inst in volume_instruments])


def make_second_line(self):
    second_line_frame = Frame(self.header_frame)
    second_line_frame.pack(
        fill="x",
        side="top"
    )


async def make_right_column(self):
    right_column = Frame(self.header_frame)

    right_column_label = ttk.Label(
        right_column,
        text="AI Settings",
        font=self.font_verdana_bold,
        justify=CENTER
    )
    right_column_label.pack(anchor='n', fill=X)
    ai_input_length_label = ttk.Label(
        right_column,
        text="Input length"
    )
    ai_input_length_label.pack(anchor='nw')
    ai_input_length = ttk.Spinbox(
        right_column,
        from_=1,
        to=10000,
        increment=100
    )
    ai_input_length.pack(anchor='nw')
    ai_output_length_label = ttk.Label(
        right_column,
        text="Output length"
    )
    ai_output_length_label.pack(anchor='nw')
    ai_output_length = ttk.Spinbox(
        right_column,
        from_=1,
        to=1000,
        increment=10
    )
    ai_output_length.pack(anchor='nw')
    ai_deep_length_label = ttk.Label(
        right_column,
        text="Deep of training"
    )
    ai_deep_length_label.pack(anchor='nw')
    ai_deep_length = ttk.Spinbox(
        right_column,
        from_=1,
        to=10000
    )
    ai_deep_length.pack(anchor='nw')

    right_column.pack(
        fill=BOTH,
        side=TOP,
        ipadx=app_styles['pad_x'],
        ipady=app_styles['pad_y']
    )
