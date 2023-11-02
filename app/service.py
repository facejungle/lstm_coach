"""
Main service for management of application
"""

import tkinter as tk
from app.features.data_loader import DataLoader
from app.shared.utils import resource_path
from app.style import make_app_fonts, make_app_style, APP_STYLE
from app.widgets.header.header import make_app_header
from app.widgets.header.menu import make_menu
from app.widgets.footer.footer import make_app_footer


class Service():
    """
    Class Service for management application
    start()
    """

    def __init__(self):
        self.app = tk.Tk()
        self.main_view = tk.Frame(
            self.app, bg=APP_STYLE['color']['app_background'])
        self.main_view.pack(fill="both", expand=True)

        self.main_frame = tk.Frame(
            self.main_view,
            bg=APP_STYLE['color']['app_background']
        )

    def start(self):
        """start app"""
        make_app_fonts(self)
        make_app_style(self)
        make_menu(self)
        make_app_header(self)
        make_app_footer(self)

        self.main_frame.pack(fill="both", expand=True)

        self.app.mainloop()

async def app_loader():
    """app loader"""
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
    # if os.name == 'nt':
    #    loader.iconwindow(resource_path("app\\res\\icon.ico"))
    loader.wm_iconbitmap(default=resource_path("res/icon.ico"))
    # loader.iconbitmap(default=resource_path("app/res/icon.ico"))
    loader.attributes('-alpha', 0.8)
    label = tk.Label(loader, text="Loading...")
    label.pack(anchor="center", fill="both", expand=True)
    DataLoader().parse_save_instruments()
    loader.after(10, start_app)
    loader.mainloop()
