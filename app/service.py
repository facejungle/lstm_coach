"""
Main service for management of application
"""
import asyncio
import tkinter as tk
from app.frames.menu import make_menu
from app.frames.header import make_app_header
from app.frames.footer import make_app_footer
from app.style.style import make_app_fonts, make_app_style, app_styles
from features.utils import resource_path
from shared.exchanges.exchanges import Exchanges


class Service():
    """
    Class Service for management application
    start()
    """

    def __init__(self):
        self.app = tk.Tk()
        self.main_view = tk.Frame(
            self.app, bg=app_styles['color']['app_background'])
        self.main_view.pack(fill=tk.BOTH, expand=True)

        self.main_frame = tk.Frame(
            self.main_view,
            bg=app_styles['color']['app_background']
        )

    def start(self):
        make_app_fonts(self)
        make_app_style(self)
        make_menu(self)
        make_app_header(self)
        make_app_footer(self)

        btn = tk.ttk.Button(self.main_frame, text="Button")
        btn.pack()
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.app.mainloop()


async def app_loader():
    def start_app():
        loader.destroy()
        Service().start()

    loader = tk.Tk()
    loader.overrideredirect(True)
    screen_width = loader.winfo_screenwidth()
    screen_height = loader.winfo_screenheight()

    window_width = 600
    window_height = 400
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    loader.geometry(f"{window_width}x{window_height}+{x}+{y}")
    loader.iconbitmap(default=resource_path("app/res/icon.ico"))
    loader.attributes('-alpha', 0.8)
    label = tk.Label(loader, text="Loading...")
    label.pack(anchor="center", fill="both", expand=True)
    Exchanges().parse_save_instruments_wrapper()
    loader.after(2000, start_app)
    loader.mainloop()
