import tkinter as tk


async def make_menu(self):
    style = tk.ttk.Style()
    app_style = style.theme_names()
    selected_theme = tk.StringVar()

    def change_theme():
        style.theme_use(selected_theme.get())

    main_menu = tk.Menu()
    self.app.option_add("*tearOff", tk.FALSE)
    file_menu = tk.Menu()
    file_menu.add_command(label="New")
    file_menu.add_command(label="Save")
    file_menu.add_command(label="Open")
    file_menu.add_separator()
    file_menu.add_command(label="Exit")

    theme_menu = tk.Menu()
    for theme in app_style:
        theme_menu.add_radiobutton(label=theme, command=change_theme, value=theme,
                                   variable=selected_theme)

    main_menu.add_cascade(label="File", menu=file_menu)
    main_menu.add_cascade(label="Edit")
    main_menu.add_cascade(label="Theme", menu=theme_menu)

    self.app.config(menu=main_menu)
