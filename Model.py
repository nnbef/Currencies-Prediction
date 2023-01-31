from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense, MaxPool1D


class LSTMmodel:
    def __init__(self):
        self.__model = Sequential()

    def build(self):
        self.__model.add(LSTM(30, input_shape=(30, 1), return_sequences=True))
        self.__model.add(Dropout(0.05))
        self.__model.add(MaxPool1D(5))
        self.__model.add(LSTM(100, return_sequences=False))
        self.__model.add(Dropout(0.05))
        self.__model.add(Dense(1, activation='linear'))
        self.__model.compile(loss='mse', optimizer='adam')

    def train(self, data, labels, epochs, batch_size):
        self.__model.fit(data, labels, epochs=epochs, batch_size=batch_size)

    def predict(self, data):
        return self.__model.predict(data)
