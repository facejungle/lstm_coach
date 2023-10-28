import asyncio
from multiprocessing import Value
from threading import Thread
from tkinter import *
from tkinter import HORIZONTAL, ttk
import json
from tkinter import font

from app.frames.header import getHeaderFrame
from features.data_loader import DataLoader
from shared.exchanges.binance import Binance


class Service():
    def __init__(self):
        self.paddingX = 10
        self.paddingY = 10
        self.appBackground = '#444444'
        self.frameBackground = '#555555'
        self.textColor = '#ffffff'
        self.textColorAlt = '#000000'
        self.AppCfg = json.load(open('config.json', 'r'))
        self.app = Tk()
        self.icon = PhotoImage(file="app/res/icon.png")
        self.app.iconphoto(False, self.icon)
        self.app.geometry(
            f"{self.AppCfg['app']['win_min_w']}x{self.AppCfg['app']['win_min_h']}+500+500")
        self.app.minsize(self.AppCfg['app']['win_min_w'],
                         self.AppCfg['app']['win_min_h'])
        self.app.title(self.AppCfg['app']['title'])
        self.View = Frame(
            self.app,
            bg=self.appBackground
        ).pack()

        self.headerFrame = Frame(
            self.View,
            bg=self.appBackground
        )

        self.mainFrame = Frame(
            self.View,
            bg=self.appBackground
        )

        self.footerFrame = Frame(
            self.View,
            bg=self.appBackground,
            height=50
        )

        self.progress = ttk.Progressbar(
            self.footerFrame, orient=HORIZONTAL, length=self.AppCfg['app']['win_min_w'] / 2, mode='determinate')

        # STYLES
        self.fontVerdana = font.Font(
            family="Verdana",
            size=11,
            weight="normal",
            slant="roman"
        )
        self.fontVerdanaSmall = font.Font(
            family="Verdana",
            size=10,
            weight="normal",
            slant="roman"
        )
        self.fontVerdanaBold = font.Font(
            family="Verdana",
            size=12,
            weight="bold",
            slant="roman"
        )
        ttk.Style().configure(
            '.',
            font=self.fontVerdana,
            foreground=self.textColor,
            padding=5,
            background=self.frameBackground
        )
        style = ttk.Style()
        appStyles = style.theme_names()
        ttk.Style().theme_use("vista")

        selected_theme = StringVar()

        def change_theme():
            style.theme_use(selected_theme.get())

        main_menu = Menu()
        self.app.option_add("*tearOff", FALSE)
        file_menu = Menu()
        file_menu.add_command(label="New")
        file_menu.add_command(label="Save")
        file_menu.add_command(label="Open")
        file_menu.add_separator()
        file_menu.add_command(label="Exit")

        theme_menu = Menu()
        for theme in appStyles:
            theme_menu.add_radiobutton(label=theme, command=change_theme, value=theme,
                                       variable=selected_theme)

        main_menu.add_cascade(label="File", menu=file_menu)
        main_menu.add_cascade(label="Edit")
        main_menu.add_cascade(label="Theme", menu=theme_menu)

        self.app.config(menu=main_menu)

    def xxx(self):
        asyncio.run(DataLoader().getInstruments())

    def test(self):
        Thread(target=self.xxx).start()

    def start(self):
        def step():
            # progress['value'] += 20
            self.progress.start(1)

        # HEADER
        getHeaderFrame(self)

        btn = ttk.Button(self.mainFrame, text="Button", command=self.test)
        btn.pack()
        self.getFooterFrame()

        self.headerFrame.pack(fill=X, side=TOP)
        self.mainFrame.pack(fill=BOTH, expand=True)
        self.footerFrame.pack(fill=X, side=BOTTOM)

        # self.app.after(0, asyncio.run, self.test())
        self.app.mainloop()

    def getFooterFrame(self):
        self.progress.pack(side=RIGHT)
