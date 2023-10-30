"""
Style for application
"""
import tkinter as tk
from tkinter import font

from features.utils import resource_path
app_styles = {
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
    tk.ttk.Style().configure(
        '.',
        font=self.font_verdana,
        foreground=app_styles['color']['text'],
        padding=5,
        background=app_styles['color']['frame_background']
    )


def make_app_style(self):
    """ Set up default style """
    self.app.iconbitmap(default=resource_path("app/res/icon.ico"))
    self.app.geometry(
        f"{app_styles['window']['min_w']}x{app_styles['window']['min_h']}+500+500")
    self.app.minsize(
        app_styles['window']['min_w'],
        app_styles['window']['min_h']
    )
    self.app.attributes('-alpha', 0.98)
    self.app.title(app_styles['window']['title'])
    style = tk.ttk.Style()
    # style.configure("Treeview", foreground=app_styles['color']['text'])
    style.theme_use("vista")
