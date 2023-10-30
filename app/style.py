"""
Style for application
"""
from tkinter import font, ttk
APP_STYLE = {
    "pad_x": 10,
    "pad_y": 10,
    "color": {
        "app_background": "#ccc",
        "frame_background": "#eee",
        "text": "#000",
        "text_alt": "#ffffff"
    },
    "window": {
        "title": "RNN LSTM AI [Coach application]",
        "min_w": 900,
        "min_h": 500,
        "max_w": 1920,
        "max_h": 1080
    }
}


def make_app_fonts(self):
    """ general style for app"""
    self.font_verdana = font.Font(
        family="Verdana",
        size=10,
        weight="normal",
        slant="roman"
    )
    self.font_verdana_small = font.Font(
        family="Verdana",
        size=8,
        weight="normal",
        slant="roman"
    )
    self.font_verdana_bold = font.Font(
        family="Verdana",
        size=12,
        weight="bold",
        slant="roman"
    )
    ttk.Style().configure(
        '.',
        font=self.font_verdana,
        foreground=APP_STYLE['color']['text'],
        padding=5,
        background=APP_STYLE['color']['frame_background']
    )


def make_app_style(self):
    """ Set up default style """
    # self.app.iconbitmap(default=resource_path("app/res/icon.ico"))
    self.app.geometry(
        f"{APP_STYLE['window']['min_w']}x{APP_STYLE['window']['min_h']}+500+500")
    self.app.minsize(
        APP_STYLE['window']['min_w'],
        APP_STYLE['window']['min_h']
    )
    self.app.attributes('-alpha', 0.98)
    self.app.title(APP_STYLE['window']['title'])
    style = ttk.Style()
    style.theme_use("clam")
