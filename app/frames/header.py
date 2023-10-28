from tkinter import BOTH, CENTER, LEFT, TOP, X, Frame, StringVar, ttk

from shared.exchanges.binance import Binance


def getHeaderFrame(self):
    # LEFT COLUMN
    leftColumn = Frame(self.headerFrame, bg=self.frameBackground)
    languages = ["Python", "JavaScript", "C#",
                 "Java", "Python", "JavaScript", "C#", "Java"]
    languages_var = StringVar(value=languages[0]).set(languages[0])
    dataLabel = ttk.Label(
        leftColumn,
        text="Data",
        font=self.fontVerdanaBold,
        justify=CENTER
    ).pack(anchor='n', fill=X)
    instrumentsLabel = ttk.Label(
        leftColumn,
        text="Instrument",
        justify=CENTER
    ).pack(anchor='center', fill=X)
    instrumentsField = ttk.Combobox(
        leftColumn,
        values=languages,
        height=5,
        textvariable=languages_var,
        state='readonly',
        foreground=self.textColorAlt
    ).pack()

    volumeLabel = ttk.Label(
        leftColumn,
        text="Volume",
        justify=CENTER
    ).pack(anchor='center', fill=X)

    volumeField = ttk.Combobox(
        leftColumn,
        values=languages,
        height=5,
        textvariable=languages_var,
        state='readonly',
        foreground=self.textColorAlt
    ).pack()

    additionalLabel = ttk.Label(
        leftColumn,
        text="Additional",
        justify=CENTER
    ).pack(anchor='center', fill=X)

    additionalField = ttk.Combobox(
        leftColumn,
        values=languages,
        height=5,
        textvariable=languages_var,
        state='readonly',
        foreground=self.textColorAlt
    ).pack()

    leftColumn.pack(
        anchor='center',
        fill=BOTH,
        side=LEFT,
        ipadx=self.paddingX,
        ipady=self.paddingY
    )
    # RIGHT COLUMN
    rightColumn = Frame(self.headerFrame, bg=self.frameBackground)

    aiSettingsLabel = ttk.Label(
        rightColumn,
        text="AI Settings",
        font=self.fontVerdanaBold,
        justify=CENTER
    ).pack(anchor='n', fill=X)
    aiInputLengthLabel = ttk.Label(
        rightColumn,
        text="Input length"
    ).pack(anchor='nw')
    aiInputLength = ttk.Spinbox(
        rightColumn,
        from_=1,
        to=1000,
        foreground=self.textColorAlt
    ).pack(anchor='nw')
    aiOutputLengthLabel = ttk.Label(
        rightColumn,
        text="Output length"
    ).pack(anchor='nw')
    aiOutputLength = ttk.Spinbox(
        rightColumn,
        from_=1,
        to=100,
        foreground=self.textColorAlt
    ).pack(anchor='nw')
    aiDeepLengthLabel = ttk.Label(
        rightColumn,
        text="Deep of training"
    ).pack(anchor='nw')
    aiDeepLength = ttk.Spinbox(
        rightColumn,
        from_=1,
        to=10000,
        foreground=self.textColorAlt
    ).pack(anchor='nw')

    rightColumn.pack(
        fill=BOTH,
        side=TOP,
        ipadx=self.paddingX,
        ipady=self.paddingY
    )
