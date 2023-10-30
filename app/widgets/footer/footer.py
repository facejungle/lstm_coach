from tkinter import ttk

from app.style import APP_STYLE


def make_app_footer(self):
    self.footer_frame = ttk.Frame(
        self.main_view,
        height=50
    )
    self.footer_frame.pack(fill="x", side="bottom")

    def step():
        # progress['value'] += 20
        progress.start(1)
    progress = ttk.Progressbar(
        self.footer_frame, orient="horizontal", length=APP_STYLE['window']['min_w'] / 2, mode='determinate')
    progress.pack(side="right")
