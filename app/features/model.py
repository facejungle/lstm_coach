"""AI Model"""


class AiModel():
    """AI Model"""

    def __init__(
        self,
        input_length: int,
        output_divider: int,
        deep_training: int
    ) -> None:
        self.input_length = input_length
        self.output_divider = output_divider
        self.deep_training = deep_training
        print(self.input_length)

    def start_training(self):
        """AI Model"""
        input_length:  int = int(self.input_length)
        output_length: int = int(input_length / self.output_divider)
        io_length:     int = int(input_length + output_length)
        deep_training: int = int(self.deep_training - io_length)
        array_length:  int = int((deep_training // io_length) * io_length)

    def print_result(self):
        """AI Model"""
        1
