from tkinter import ttk
from app.style import APP_STYLE


def make_second_line(self):
    second_line_frame = ttk.Frame(self.header_frame)
    second_line_frame.pack(
        fill="x",
        side="top"
    )
# INPUT LENGTH
    input_length_frame = ttk.Frame(second_line_frame)
    input_length_frame.pack(
        anchor="w",
        side="left",
        padx=APP_STYLE['pad_x'],
        pady=APP_STYLE['pad_y'],
    )
    input_length_label = ttk.Label(
        input_length_frame,
        text="Input length",
        background="#ccc",
    )
    input_length_label.pack(side="top", anchor="n", fill="x")
    input_length_field = ttk.Spinbox(
        input_length_frame,
        from_=10,
        to=1000,
        increment=10
    )
    input_length_field.pack(side='bottom', anchor="s")
# OUTPUT LENGTH
    output_length_frame = ttk.Frame(second_line_frame)
    output_length_frame.pack(
        anchor="w",
        side="left",
        padx=APP_STYLE['pad_x'],
        pady=APP_STYLE['pad_y'],
    )
    output_length_label = ttk.Label(
        output_length_frame,
        text="Output length",
        background="#ccc",
    )
    output_length_label.pack(side="top", anchor="n", fill="x")
    output_length_field = ttk.Spinbox(
        output_length_frame,
        from_=10,
        to=1000,
        increment=10
    )
    output_length_field.pack(side='bottom', anchor="s")
# DEEP OF TRAINING
    training_length_frame = ttk.Frame(second_line_frame)
    training_length_frame.pack(
        anchor="w",
        side="left",
        padx=APP_STYLE['pad_x'],
        pady=APP_STYLE['pad_y'],
    )
    training_length_label = ttk.Label(
        training_length_frame,
        text="Deep of training",
        background="#ccc",
    )
    training_length_label.pack(side="top", anchor="n", fill="x")
    training_length_field = ttk.Spinbox(
        training_length_frame,
        from_=100,
        to=10000,
        increment=100
    )
    training_length_field.pack(side='bottom', anchor="s")

    def start_training():
        inputs = input_length_field.get()
        # AiModel(inputs, 200, 444)
    btn = ttk.Button(second_line_frame, text="Button", command=start_training)
    btn.pack(anchor="e", expand=True)
