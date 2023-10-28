from tkinter import HORIZONTAL, SOLID, ttk
import tkinter as tk

class Frames():
    def __init__(self):
        self.headerFrame = tk.Frame(self.app, bg='#cccccc', borderwidth=1, relief=SOLID, padx=10, pady=5)
        self.mainFrame = tk.Frame(self.app, bg='#eeeeee', borderwidth=1, relief=SOLID, padx=10, pady=5)
        self.footerFrame =tk.Frame(self.app, bg='#cccccc', borderwidth=1, relief=SOLID, padx=10, pady=5, height=50)
    
    

