import tkinter
from okx.MarketData import MarketAPI
import numpy as np
from tensorflow import keras
from keras.layers import LSTM, Dense, Embedding, Dropout
import matplotlib.pyplot as plt


import requests

INSTRUMENT:     str = 'EOS-USD-SWAP'
TIMEFRAME:      str = '1H'
INPUT_LENGTH:   int = 48
OUT_LENGTH:     int = int(INPUT_LENGTH / 4)
IO_LENGTH:      int = int(INPUT_LENGTH + OUT_LENGTH)
DEPTH_TRAINING: int = int(4000 - IO_LENGTH)
url = "https://www.binance.com/api/v3/klines?symbol=BTCUSDC&interval=1h"

payload={}
headers = {
  'Accept': 'text/plain',
  'X-CoinAPI-Key': '<API_KEY_VALUE>'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

















market = MarketAPI()


ARRAY_LENGTH:   int = (DEPTH_TRAINING // IO_LENGTH) * IO_LENGTH
if ARRAY_LENGTH > DEPTH_TRAINING:
    ARRAY_LENGTH -= IO_LENGTH

##
#       FUNCTON BLOCK
##
def getCandles(instrument, timeframe):
    candles = market.get_history_candlesticks(instId=instrument, bar=timeframe, limit='100').get('data')
    while len(candles) < DEPTH_TRAINING:
        data = market.get_history_candlesticks(instId=instrument, bar=timeframe, limit='100', after=str(candles[-1][0]))
        candles.extend(data.get('data'))
    return candles

def get_train_data(self, seq_len, normalise):
    '''
    Create x, y train data windows
    Warning: batch method, not generative, make sure you have enough memory to
    load data, otherwise use generate_training_window() method.
    '''
    data_x = []
    data_y = []
    for i in range(self.len_train - seq_len + 1):
        x, y = self._next_window(i, seq_len, normalise)
        data_x.append(x)
        data_y.append(y)
    return np.array(data_x), np.array(data_y)

def de_normalise_predicted(self, price_1st, _data):
    return (_data + 1) * price_1st

candels = getCandles(INSTRUMENT, TIMEFRAME)
prices = [round((float(candel[1]) + float(candel[4])) / 2, 4) for candel in candels]
prices.reverse()
trainingPrices = prices[:-IO_LENGTH]

x = np.array([])
y = np.array([])
x, y = get_train_data(seq_len=48, normalise=True)
for i in range(0, int(ARRAY_LENGTH), IO_LENGTH):
    x = np.concatenate(np.array([trainingPrices[i:i+INPUT_LENGTH]]))
    y = np.concatenate(np.array([trainingPrices[i+INPUT_LENGTH:i+IO_LENGTH]]))
    
x = x.reshape(-1, INPUT_LENGTH, 1)
y = y.reshape(-1, OUT_LENGTH)

x = x[np.random.choice(x.shape[0], size=x.shape[0], replace=False)]
y = y[np.random.choice(y.shape[0], size=y.shape[0], replace=False)]

model = keras.Sequential()
model.add(LSTM(48, input_shape=(INPUT_LENGTH, 1), return_sequences=True))
model.add(Dropout(.2))
model.add(LSTM(48, return_sequences=True))
model.add(LSTM(48, return_sequences=False))
model.add(Dropout(.2))
model.add(Dense(units=OUT_LENGTH, activation='linear')) 
model.summary()
model.compile(loss='mean_squared_error', optimizer=keras.optimizers.Adam(lr=0.001), metrics=["accuracy"])
history = model.fit(x, y, batch_size=48, epochs=2000, verbose=0)
print('All Done.')

predictSample = np.array(prices[-IO_LENGTH:-OUT_LENGTH])
next_number = model.predict(predictSample.reshape(-1, INPUT_LENGTH, 1))

print('Weights: \n', model.get_weights())

predictPrices = next_number[0]
print('\n Predict prices: \n', predictPrices)

realPrices = prices[-OUT_LENGTH:]
print('\n Real prices: \n', realPrices)

win = tkinter.Tk()
win.geometry(f"300x400+100+200")
win.title('LST RNN AI')


plt.subplot(4, 1, 1)
plt.plot(np.concatenate((predictSample, predictPrices), axis=0), color='red')
plt.subplot(4, 1, 2)
plt.plot(np.concatenate((predictSample, realPrices), axis=0), color='blue')
plt.subplot(4, 1, 3)
plt.plot(history.history['loss'], color='red')
plt.subplot(4, 1, 4)
plt.plot(history.history['accuracy'], color='blue')

plt.grid(True)
plt.show()

win.mainloop()