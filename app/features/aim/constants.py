from keras.optimizers import Adam, SGD, RMSprop, Adagrad, Adadelta, Adamax, Nadam, Ftrl
from keras.layers import LSTM, GRU, SimpleRNN, Dense, Dropout, Conv1D, Conv2D, Conv3D, MaxPooling2D, BatchNormalization

LOSS_FUNCTIONS = ['mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error',
                  'mean_squared_logarithmic_error', 'cosine_similarity', 'huber',
                  'log_cosh', 'binary_crossentropy', 'categorical_crossentropy',
                  'sparse_categorical_crossentropy', 'poisson', 'kl_divergence',
                  'hinge', 'squared_hinge', 'categorical_hinge']

OPTIMIZERS = {
    'adam': Adam,
    'sgd': SGD,
    'rmsprop': RMSprop,
    'adagrad': Adagrad,
    'adadelta': Adadelta,
    'adamax': Adamax,
    'nadam': Nadam,
    'ftrl': Ftrl
}

LAYER_TYPES = {
    'lstm': {
        "class": LSTM,
        "args": ["units", "input_shape", "dropout"]
    },
    'gru': {
        "class": GRU,
        "args": ["units", "input_shape", "dropout"]
    },
    'simple_rnn': {
        "class": SimpleRNN,
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
