import tensorflow as tf
from keras.layers import LSTM, Dense, Embedding, Input
from keras.models import Sequential

class LSTMModel:
    # sigmoid -> binary
    # softmax -> multi-class
    @staticmethod
    def getUncompiledModel(inputLength, outputShape, memoryunits = 128, activation="sigmoid", embedding=True, embeddingInputDim=1000, embeddingOutputDim=32):
        model = Sequential()
        model.add(Input(inputLength))
        if embedding:
            model.add(Embedding(input_dim=embeddingInputDim, output_dim=embeddingOutputDim, input_length=inputLength))
        model.add(LSTM(memoryunits))
        model.add(Dense(outputShape, activation=activation))
        model.summary()
        return model

    @staticmethod
    def getCompiledModel(model, loss="binary_crossentropy", optimizer="adam", metrics=["accuracy", "mse", "mae"]):
        model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
        return model
