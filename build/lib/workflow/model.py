#################################
#  1 - Imports  #
#################################

import numpy as np
from tensorflow.keras import models, layers, optimizers
from tensorflow.keras.optimizers.schedules import ExponentialDecay
from tensorflow.keras.callbacks import EarlyStopping
from workflow.utils import simple_time_and_memory_tracker
from workflow.params import batch_size, epochs, patience

#################################
#  2.1 - Model - Classification #
#################################

def init_model(X_train,y_train):
    model = models.Sequential()

    # LSTM layers
    model.add(layers.LSTM(units=80, activation='relu', input_shape=X_train[0].shape ,return_sequences=True))

    model.add(layers.LSTM(units=60, activation='relu',return_sequences=True))

    model.add(layers.LSTM(units=40, activation='relu',return_sequences=True))

    model.add(layers.LSTM(units=20, activation='relu',return_sequences=True))

    # Predictive Dense Layer
    model.add(layers.Dense(3, activation='softmax'))

    return model

#################################
#  2.2 - Model - Regression #
#################################

def init_model_linear(X_train,y_train):
    model = models.Sequential()

    # LSTM layers
    model.add(layers.LSTM(units=20, activation='relu', input_shape=X_train[0].shape ,return_sequences=True))

    model.add(layers.LSTM(units=20, activation='relu',return_sequences=True))

    model.add(layers.LSTM(units=10, return_sequences=False))

    model.add(layers.Dense(10, activation='relu'))

    # Predictive Dense Layer
    model.add(layers.Dense(7, activation='linear'))

    return model

#################################
# 3 - Compile - Classification  #
#################################

def compile_model(model):

    initial_learning_rate = 0.001
    lr_schedule = ExponentialDecay(initial_learning_rate, decay_steps=1000, decay_rate=0.0001)

    opt = optimizers.Adam(learning_rate=lr_schedule)
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer= opt,
                  metrics=['sparse_categorical_accuracy'])

    return model

#################################
# 3 - Compile - Regression #
#################################

def compile_model_linear(model):

    initial_learning_rate = 0.001

    opt = optimizers.Adam(learning_rate=initial_learning_rate)
    model.compile(loss='mse',
                  optimizer= opt,
                  metrics=['mae'])

    return model

#################################
#  4 - Train  #
#################################

@simple_time_and_memory_tracker
def fit_model(model,
                X_train,
                y_train,
                validation_split=0.3,
                batch_size=batch_size,
                epochs=epochs,
                patience=patience):

    es = EarlyStopping(monitor="val_loss",
                       patience=patience,
                       restore_best_weights=True)

    history = model.fit(X_train,
                        y_train,
                        validation_split=validation_split,
                        shuffle=False,
                        batch_size=batch_size,
                        epochs=epochs,
                        callbacks=[es],
                        verbose=1)

    return model, history

#################################
#  5 - Evaluate #
#################################

def evaluate_model(model,
                   X_test,
                   y_test):

    if model is None:
        print(f"\n??? no model to evaluate")
        return None

    metrics = model.evaluate(
        X_test,
        y_test)

    loss = metrics[0]
    accuracy = metrics[1]

    print(f"??? Model evaluated: loss {round(loss, 2)} accuracy {round(accuracy, 2)}")

    return metrics

#################################
#  6 - Predict #
#################################

# def predict(model, X_test):
#     '''
#     Makes a probability prediction for each ATMO class, for each day of the output length
#     '''

#     y_pred = np.round(model.predict(X_test),2)

#     return y_pred
