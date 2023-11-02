"""AI Model"""
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Conv1D, Conv2D, Conv3D, MaxPooling2D, BatchNormalization
import numpy as np

from app.shared.exchanges.binance import Binance

LOSS_FUNCTIONS = ['mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error',
                  'mean_squared_logarithmic_error', 'cosine_similarity', 'huber',
                  'log_cosh', 'binary_crossentropy', 'categorical_crossentropy',
                  'sparse_categorical_crossentropy', 'poisson', 'kl_divergence',
                  'hinge', 'squared_hinge', 'categorical_hinge']

OPTIMIZERS = ['adam', 'sgd', 'rmsprop', 'adagrad',
              'adadelta', 'adamax', 'nadam', 'ftrl']

LAYER_TYPES = {
    'lstm': {
        "class": LSTM,
        "args": ["units", "input_shape", "dropout"]
    },
    'dense': {
        "class": Dense,
        "args": ["units"]
    },
    'dropout': {
        "class": Dropout,
        "args": ["rate"]
    },
    'conv1d': {
        "class": Conv1D,
        "args": ["filters", "kernel_size"]
    },
    'conv2d': {
        "class": Conv2D,
        "args": ["filters", "kernel_size"]
    },
    'conv3d': {
        "class": Conv3D,
        "args": ["filters", "kernel_size"]
    },
    'maxpooling2d': {
        "class": MaxPooling2D,
        "args": ["pool_size"]
    },
    'batchnormalization': {
        "class": BatchNormalization,
        "args": []
    }
}


class AiModel():
    def __init__(self, configuration: dict) -> None:
        if not isinstance(configuration, dict):
            raise ValueError("Configuration must be a dictionary.")
        self.model = Sequential()
        self.config = configuration
        if "data" not in self.config or not isinstance(self.config["data"], list):
            raise ValueError(
                "Data must be provided in the configuration as a list.")
        self.data: list = self.config["data"]
        if "xy_length" not in self.config or not isinstance(self.config["xy_length"], int):
            raise ValueError(
                "xy_length must be provided in the configuration as an integer.")
        self.train_data: list = self.config["data"][:-self.config["xy_length"]]

    def add_layer(self, layer_config):
        if not isinstance(layer_config, dict) or 'type' not in layer_config or 'params' not in layer_config:
            raise ValueError(
                "Layer config must be a dictionary with 'type' and 'params'.")
        layer_type = layer_config['type']
        if layer_type not in LAYER_TYPES:
            raise ValueError(f"{layer_type} is not a valid layer type.")
        layer_class = LAYER_TYPES[layer_type]["class"]
        layer_params = {arg: layer_config['params'][arg]
                        for arg in LAYER_TYPES[layer_type]["args"] if arg in layer_config['params']}
        layer = layer_class(**layer_params)
        self.model.add(layer)

    def build_model(self):
        if "layers" not in self.config or not isinstance(self.config["layers"], list):
            raise ValueError(
                "Layers must be provided in the configuration as a list.")
        for layer_config in self.config["layers"]:
            self.add_layer(layer_config)

    def compile_model(self):
        optimizer = self.config.get('optimizer')
        loss = self.config.get('loss')
        if optimizer is None or loss is None:
            raise ValueError(
                "Both optimizer and loss must be provided in the configuration.")
        if optimizer not in OPTIMIZERS:
            raise ValueError(f"{optimizer} is not a valid optimizer.")
        if loss not in LOSS_FUNCTIONS:
            raise ValueError(f"{loss} is not a valid loss function.")
        self.model.compile(loss=loss, optimizer=optimizer)

    def start_training(self):
        if not isinstance(self.model, Sequential):
            print("Model not built. Call build_model() first.")
            return
        x = []
        y = []
        for i in range(0, len(self.train_data) - self.config["xy_length"]):
            x.append(self.train_data[i:i+self.config["x_train_length"]])
            y.append(
                self.train_data[i+self.config["x_train_length"]:i+self.config["xy_length"]])
        x_train = np.array(x).reshape(-1, self.config["x_train_length"])
        x_train = x_train.reshape(
            (x_train.shape[0], x_train.shape[1], 1)).astype(float)
        y_train = np.array(
            y).reshape(-1, self.config["y_train_length"], 1).astype(float)

        history = self.model.fit(x_train, y_train, epochs=self.config.get("epochs", 1),
                                 batch_size=self.config.get("batch_size", 32))
        return history


datas = Binance().parse_candles('BTCUSDC', '1h', 5000)
config = {
    "data": [data[4] for data in datas],
    "x_train_length": 48,
    "y_train_length": 12,
    "xy_length": 60,
    "deep_training": 5000,
    "layers": [
        {
            "type": "lstm",
            "params": {
                "units": 48,
                "input_shape": (48, 1),
                "return_sequences": True
            }
        },
        {
            "type": "dropout",
            "params": {
                "rate": .2
            }
        },
        {
            "type": "lstm",
            "params": {
                "units": 48,
                "input_shape": (48, 1),
                "return_sequences": True
            }
        },
        {
            "type": "lstm",
            "params": {
                "units": 48,
                "input_shape": (48, 1),
                "return_sequences": False
            }
        },
        {
            "type": "dropout",
            "params": {
                "rate": .2
            }
        },
        {
            "type": "dense",
            "params": {
                "units": 12,
                "activation": "linear"
            }
        }
    ],

    "loss": 'mean_squared_error',
    "optimizer": "adam",


    "epochs": 10,
    "batch_size": 32
}
model = AiModel(config)


model.build_model()
model.compile_model()
historyx = model.start_training()
print(historyx)
