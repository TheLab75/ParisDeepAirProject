#############################
#  1 - package  #
#############################

import os
import tensorflow
from tensorflow import keras
import time
import numpy as np

from tensorflow.keras.layers import SimpleRNN, LSTM, GRU
from tensorflow.keras import optimizers
from keras.layers import Input, Flatten
from tensorflow.keras import Sequential, layers
from tensorflow.keras.callbacks import EarlyStopping
from keras.optimizers.optimizer_experimental import optimizer


#############################
#  2 - Model  #
#############################


def init_model(X):

    model = models.Sequential()

    model.add(layers.LSTM(200, activation='relu', input_dim=3, return_sequence = True)) # 1st hidden layer with 200 neurons
    #model.add(layers.Dropout(rate=0.1)) # droupout layer 10%

    model.add(layers.LSTM(100, activation='relu')) # 2st hidden layer with 100 neurons
    model.add(layers.Dropout(rate=0.1)) # droupout layer 10%

    model.add(layers.LSTM(50, activation='relu'))
    model.add(layers.Dropout(rate=0.1)) # droupout layer 10%

    model.add(layers.LSTM(50, activation='relu'))
    model.add(layers.Dropout(rate=0.1)) # droupout layer 10%

    model.add(Flatten())

    model.add(layers.Dense(6, activation='softmax')) # Output layer that outputs a probability of belonging to the class of "success"

    return model


    #############################
    # 3 - compile  #
    #############################


def compile_model(model):

    opt = optimizers.Adam(learning_rate=0.001, decay_rate=0.0001)
    model.compile(loss='categorical_crossentropy',
                  optimizer= opt,
                  metrics=['accuracy'])

    return model

    #############################
    #  4 - train  #
    #############################

def train_model(model,
                X_train,
                y_train,
                batch_size=64,
                patience=50,
                validation_split=0.3,
                validation_data=None):

    es = EarlyStopping(patience=patience,
                       restore_best_weights=True,
                       verbose=1)

    history = model.fit(X_train,
                        y_train,
                        validation_split=validation_split,
                        validation_data=validation_data,
                        epochs=200,
                        batch_size=batch_size,
                        callbacks=[es],
                        verbose=0)
    return model, history

    #############################
    #  5 - evaluat  #
    #############################

def evaluate_model(model,
                   X_test,
                   y_test,
                   batch_size=32):

    if model is None:
        print(f"\n❌ no model to evaluate")
        return None

    metrics = model.evaluate(
        X_test,
        y_test,
        batch_size=batch_size,
        verbose=1,
        # callbacks=None,
        return_dict=True)

    loss = metrics["loss"]
    accuracy = metrics["accuracy"]

    print(f"\n✅ model evaluated: loss {round(loss, 2)} accuracy {round(accuracy), 2)}")

    return metrics
