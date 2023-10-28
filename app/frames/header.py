"""Module providing a function to print the Python version."""
import asyncio
from tkinter import BOTH, CENTER, LEFT, TOP, X, Frame, StringVar, ttk
from app.style.style import app_styles


async def make_app_header(self):
    """Module providing a function to print the Python version."""
    self.header_frame = Frame(
        self.main_view,
        bg=app_styles['color']['app_background']
    )
    self.header_frame.pack(fill=X, side=TOP)
    await asyncio.gather(make_left_column(self), make_right_column(self))


async def make_left_column(self):
    """Left column for header app."""
    left_column = Frame(self.header_frame,
                        bg=app_styles['color']['frame_background'])
    languages = ["Python", "JavaScript", "C#",
                 "Java", "Python", "JavaScript", "C#", "Java"]
    languages_var = StringVar(value=languages[0]).set(languages[0])
    left_column_label = ttk.Label(
        left_column,
        text="Data",
        font=self.font_verdana_bold,
        justify=CENTER
    )
    left_column_label.pack(anchor='n', fill=X)
    instruments_label = ttk.Label(
        left_column,
        text="Instrument",
        justify=CENTER
    )
    instruments_label.pack(anchor='center', fill=X)
    instruments_field = ttk.Combobox(
        left_column,
        values=languages,
        height=5,
        textvariable=languages_var,
        state='readonly',
        foreground=app_styles['color']['text_alt']
    )
    instruments_field.pack()

    volume_label = ttk.Label(
        left_column,
        text="Volume",
        justify=CENTER
    )
    volume_label.pack(anchor='center', fill=X)

    volume_field = ttk.Combobox(
        left_column,
        values=languages,
        height=5,
        textvariable=languages_var,
        state='readonly',
        foreground=app_styles['color']['text_alt']
    )
    volume_field.pack()

    additional_label = ttk.Label(
        left_column,
        text="Additional",
        justify=CENTER
    )
    additional_label.pack(anchor='center', fill=X)

    additional_field = ttk.Combobox(
        left_column,
        values=languages,
        height=5,
        textvariable=languages_var,
        state='readonly',
        foreground=app_styles['color']['text_alt']
    )
    additional_field.pack()

    left_column.pack(
        anchor='center',
        fill=BOTH,
        side=LEFT,
        ipadx=app_styles['pad_x'],
        ipady=app_styles['pad_y']
    )


async def make_right_column(self):
    right_column = Frame(
        self.header_frame, bg=app_styles['color']['frame_background'])

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
        to=1000,
        foreground=app_styles['color']['text_alt']
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
        to=100,
        foreground=app_styles['color']['text_alt']
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
        to=10000,
        foreground=app_styles['color']['text_alt']
    )
    ai_deep_length.pack(anchor='nw')

    right_column.pack(
        fill=BOTH,
        side=TOP,
        ipadx=app_styles['pad_x'],
        ipady=app_styles['pad_y']
    )
