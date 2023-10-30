from tkinter import StringVar, ttk
from app.features.data_loader import DataLoader
from app.style import APP_STYLE


def make_first_line(self):
    """Make first line on header for app."""
    first_line_frame = ttk.Frame(self.header_frame)
    first_line_frame.pack(
        fill="x",
        side="top"
    )

# EXCHANGE FRAME
    exchange_frame = ttk.Frame(first_line_frame)
    exchange_frame.pack(
        anchor="w",
        side="left",
        padx=APP_STYLE['pad_x'],
        pady=APP_STYLE['pad_y'],
    )
    exchange_label = ttk.Label(
        exchange_frame,
        text="Exchange",
        background="#ccc",
    )
    exchange_label.pack(side="top", anchor="n", fill="x")
    exchanges = DataLoader().get_exchanges_list()
    exchange_var = StringVar(value=exchanges[0])

    def choice_exchange():
        exchange_selection = exchange_field.get()
        market_field.set('')
        instruments_field.set('')
        if exchange_selection in exchanges:
            instruments = DataLoader().get_instruments_from_csv(exchange_selection)
            exchange_markets = instruments['market'].unique()
            market_field.configure(
                values=list(exchange_markets))

    def choice_market():
        market_selection = market_field.get()
        instruments_field.set('')
        exchange_selection = exchange_field.get()
        if exchange_selection in exchanges:
            instruments = DataLoader().get_instruments_from_csv(exchange_selection)
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
    market_frame = ttk.Frame(first_line_frame)
    market_frame.pack(
        anchor="w",
        side="left",
        padx=APP_STYLE['pad_x'],
        pady=APP_STYLE['pad_y'],
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
    instruments_frame = ttk.Frame(first_line_frame)
    instruments_frame.pack(
        anchor="w",
        side="left",
        padx=APP_STYLE['pad_x'],
        pady=APP_STYLE['pad_y'],
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
    volume_frame = ttk.Frame(first_line_frame)
    volume_frame.pack(
        anchor="w",
        side="left",
        padx=APP_STYLE['pad_x'],
        pady=APP_STYLE['pad_y'],
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
    # volume_instruments = new_thread(
    # DataLoader().get_volume_instruments, ["2"])

    # volume_field.configure(values=[inst[1]
    #                               for inst in volume_instruments])
