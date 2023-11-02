"""
\n The AiModel class is designed to create and train a deep
\n learning model using the Keras library.

\n Class constructor. Accepts model configuration as a dictionary.
\n Initializes the model, scales the data, and prepares the training data.
"""
from app.features.aim.constants import LAYER_TYPES, LOSS_FUNCTIONS, OPTIMIZERS
from app.shared.utils import resource_path

import datetime
from keras import regularizers
from keras.models import Sequential
import numpy as np


class AiModel():
    """
    \n The AiModel class is designed to create and train a deep
    \n learning model using the Keras library.

    \n Class constructor. Accepts model configuration as a dictionary.
    \n Initializes the model, scales the data, and prepares the training data.
    """

    def __init__(self, config):
        self.config = config
        self.model = Sequential()
        self.inputs_train, self.outputs_train = prepare_data_rnn(
            self.config['data'], self.config['x_length'], self.config['y_length'])
        self.__build_model()

    def __add_layer(self, layer_config, layer_index):
        """
        \n Adds a layer to the model based on the layer configuration.
        \n Verifies that all required parameters are provided and supported.
        """
        layer_type = layer_config['type']
        if layer_type not in LAYER_TYPES:
            raise ValueError(f"Unsupported layer type: {layer_type}")

        layer_class = LAYER_TYPES[layer_type]["class"]
        layer_params = layer_config['params']

        # Check if all required parameters are provided
        for arg in LAYER_TYPES[layer_type]["args"]:
            if arg not in layer_params and not (arg == 'input_shape' and layer_index > 0):
                raise ValueError(
                    f"Missing required parameter {arg} for layer type {layer_type}")

        # Handle regularizers
        if 'regularizers' in layer_params:
            reg_params = layer_params.pop('regularizers')
            for reg_type, reg_config in reg_params.items():
                if reg_type == 'kernel_regularizer':
                    layer_params['kernel_regularizer'] = regularizers.l1_l2(
                        **reg_config)
                elif reg_type == 'bias_regularizer':
                    layer_params['bias_regularizer'] = regularizers.l2(
                        reg_config)
                elif reg_type == 'activity_regularizer':
                    layer_params['activity_regularizer'] = regularizers.l2(
                        reg_config)

        layer = layer_class(**layer_params)
        self.model.add(layer)

    def __build_model(self):
        """
        \n Builds the model by adding layers according to the configuration and compiles
        \n the model with the given loss function and optimizer.
        """
        for i, layer_config in enumerate(self.config["layers"]):
            print(layer_config)
            self.__add_layer(layer_config, i)

        compiler_config = self.config["compiler"]

        optimizer_config = compiler_config.get("optimizer", {})
        optimizer_type = list(optimizer_config.keys())[0]

        if optimizer_type not in OPTIMIZERS:
            raise ValueError(f"Unsupported optimizer: {optimizer_type}")

        optimizer_class = OPTIMIZERS[optimizer_type]
        optimizer = optimizer_class(**optimizer_config[optimizer_type])

        loss_function = compiler_config.get("loss")

        if loss_function not in LOSS_FUNCTIONS:
            raise ValueError(f"Unsupported loss function: {loss_function}")

        metrics_list = compiler_config.get("metrics", [])

        self.model.compile(
            loss=loss_function, optimizer=optimizer, metrics=metrics_list)

    def train_model(self, data=None):
        """
        \n Trains the model on training data.
        \n If other data is provided, it uses them instead of training data.
        \n "data" is a tuple of two numpy arrays (input and output data)
        """
        x, y = self.inputs_train, self.outputs_train
        if data is not None and len(data) == 2:
            x, y = data

        epochs_value = self.config.get("epochs")
        batch_size_value = self.config.get("batch_size")
        validation_split_value = self.config.get("validation_split")
        shuffle_value = self.config.get("shuffle")
        return self.model.fit(
            x, y,
            epochs=epochs_value,
            batch_size=batch_size_value,
            validation_split=validation_split_value,
            shuffle=shuffle_value
        )

    def save_model(self):
        """Saves the trained model to a .h5 file"""
        now = datetime.datetime.now()
        file_name = f'model_{now.strftime("%Y%m%d_%H%M%S")}.h5'
        self.model.save(resource_path(f"data/models/{file_name}"))


def prepare_data_rnn(data, x_length: int, y_length: int):
    """
    \n Prepares data for training the model.
    \n Splits data into input and output data.
    \n Returns a tuple of two numpy arrays (input and output data)
    """
    xy_length = x_length + y_length
    deep_train = len(data) - xy_length
    array_length = (deep_train // xy_length) * xy_length
    if array_length > deep_train:
        array_length -= xy_length
    samples = list(data)[:array_length]
    inputs, outputs = split_array(samples, x_length, y_length)

    n_features = len(data[0])
    n_windows = array_length // xy_length

    inputs = np.reshape(inputs, (n_windows, x_length, n_features))
    outputs = np.reshape(outputs, (n_windows, y_length * n_features))
    return inputs, outputs


def normalize(data):
    """
    \n Normalizes data using Min-Max normalization.
    \n Returns a tuple of three numpy arrays:
    \n (normalized data, minimum feature values, maximum feature values)
    """
    data = np.array(data)
    min_val = np.min(data, axis=0)
    max_val = np.max(data, axis=0)
    normalized_data = (data - min_val) / (max_val - min_val)

    return normalized_data, min_val, max_val


def denormalize(normalized_data, min_val, max_val):
    """Denormalize data"""
    denormalized_data = normalized_data * (max_val - min_val) + min_val

    return denormalized_data


def split_array(data, x_length, y_length):
    """
    \n Splits an array of data into input and output data for training the model.
    \n Returns a tuple of two numpy arrays (input and output data)
    """
    xy_length = x_length + y_length
    array_length = len(data)
    inputs, outputs = [], []
    for i in range(0, int(array_length), xy_length):
        inputs.append(data[i:i+x_length])
        outputs.append(data[i+x_length:i+xy_length])
    inputs, _, _ = normalize(inputs)
    outputs, _, _ = normalize(outputs)
    return np.array(inputs), np.array(outputs)
