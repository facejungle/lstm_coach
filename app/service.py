"""
Main service for management of application
"""
import asyncio
from threading import Thread
import tkinter as tk
from app.frames.menu import make_menu
from app.frames.header import make_app_header
from app.frames.footer import make_app_footer
from app.style.style import make_app_fonts, make_app_style, app_styles
from features.data_loader import DataLoader


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

    def xxx(self):
        asyncio.run(DataLoader().getInstruments())

    def test(self):
        Thread(target=self.xxx).start()

    async def start(self):
        await asyncio.gather(
            make_app_fonts(self),
            make_app_style(self),
            make_menu(self),
            make_app_header(self),
            make_app_footer(self)
        )

        btn = tk.ttk.Button(self.main_frame, text="Button", command=self.test)
        btn.pack()

        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # self.app.after(0, asyncio.run, self.test())
        self.app.mainloop()
