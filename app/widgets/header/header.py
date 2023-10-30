from tkinter import ttk
from app.widgets.header import first_line, second_line


def make_app_header(self):
    """Module providing a function to print the Python version."""
    self.header_frame = ttk.Frame(
        self.main_view
    )
    self.header_frame.pack(fill="x", side="top")
    first_line.make_first_line(self)
    second_line.make_second_line(self)