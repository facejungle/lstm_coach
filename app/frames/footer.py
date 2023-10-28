from tkinter import BOTTOM, X, HORIZONTAL, RIGHT, Frame
from tkinter.ttk import Progressbar
from app.style.style import app_styles


async def make_app_footer(self):
    self.footer_frame = Frame(
        self.main_view,
        bg=app_styles['color']['app_background'],
        height=50
    )
    self.footer_frame.pack(fill=X, side=BOTTOM)

    def step():
        # progress['value'] += 20
        progress.start(1)
    progress = Progressbar(
        self.footer_frame, orient=HORIZONTAL, length=app_styles['window']['min_w'] / 2, mode='determinate')
    progress.pack(side=RIGHT)
