# Python file containing all the code for model evaluation

# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Tuple
from workflow.params import FOLD_LENGTH, FOLD_STRIDE, STRIDE, TRAIN_TEST_RATIO, N_FEATURES, INPUT_LENGTH, TARGET, TARGET_COLUMN_IDX, N_TARGETS, OUTPUT_LENGTH, HORIZON
from workflow.baseline import baseline
from workflow.model import init_model, compile_model, fit_model, evaluate_model

# Folding our dataset
def get_folds(df: pd.DataFrame,
              fold_length: int,
              fold_stride: int) -> List[pd.DataFrame]:
    '''
    This function slides through the Time Series dataframe of shape (n_timesteps, n_features) to create folds
    - of equal `fold_length`
    - using `fold_stride` between each fold

    Returns a list of folds, each as a DataFrame
    '''

    folds = []
    for idx in range(0, len(df), fold_stride):
        # Exits the loop as soon as the last fold index would exceed the last index
        if (idx + fold_length) > len(df):
            break
        fold = df.iloc[idx:idx + fold_length, :]
        folds.append(fold)

    print(f'Folds shape: {np.array(folds).shape}')
    print(f'The function generated {len(folds)} folds.')
    print(f'Each fold has a shape equal to {folds[0].shape}.')
    print("\n")

    return folds

# Train-test split
def train_test_split(fold: pd.DataFrame,
                     train_test_ratio: float,
                     input_length: int,
                     horizon: int) -> Tuple[pd.DataFrame]:
    '''
    Returns a train dataframe and a test dataframe (fold_train, fold_test)
    from which one can sample (X,y) sequences.
    df_train should contain all the timesteps until round(train_test_ratio * len(fold))
    '''

    # TRAIN SET
    # ======================
    last_train_idx = round(train_test_ratio * len(fold))
    fold_train = fold.iloc[0:last_train_idx, :]

    # TEST SET
    # ======================
    first_test_idx = last_train_idx - input_length
    fold_test = fold.iloc[first_test_idx:, :]

    return (fold_train, fold_test)

# Extract one sequence from a fold
def get_Xi_yi(first_index: int,
              fold: pd.DataFrame,
              horizon: int,
              input_length: int,
              output_length: int) -> Tuple[np.ndarray, np.ndarray]:
    '''
    - extracts one sub-fold from a fold
    - returns a pair (Xi, yi) with:
        * len(Xi) = `input_length` and Xi starting at first_index
        * len(yi) = `output_length`
        * last_Xi and first_yi separated by the gap = horizon -1
    '''

    Xi_start = first_index
    Xi_last = Xi_start + input_length
    yi_start = Xi_last + horizon - 1
    yi_last = yi_start + output_length

    Xi = fold[Xi_start:Xi_last]
    yi = fold[yi_start:yi_last][TARGET]

    return (Xi, yi)

# Splitting a fold into a X_train, y_train & X_test, y_test
def get_X_y(fold: pd.DataFrame,
            horizon: int,
            input_length: int,
            output_length: int,
            stride: int,
            shuffle=True) -> Tuple[np.ndarray, np.ndarray]:
    """
    - Uses `data`, a 2D-array with axis=0 for timesteps, and axis=1 for (targets+covariates columns)
    - Returns a Tuple (X,y) of two ndarrays :
        * X.shape = (n_samples, input_length, n_covariates)
        * y.shape =
            (n_samples, output_length, n_targets) if all 3-dimensions are of size > 1
            (n_samples, output_length) if n_targets == 1
            (n_samples, n_targets) if output_length == 1
            (n_samples, ) if both n_targets and lenghts == 1
    - You can shuffle the pairs (Xi,yi) of your fold
    """

    X = []
    y = []

    # Scanning the fold/data entirely with a certain stride
    for i in range(0, len(fold), stride):
        ## Extracting a sequence starting at index_i
        Xi, yi = get_Xi_yi(first_index=i,
                           fold=fold,
                           horizon=horizon,
                           input_length=input_length,
                           output_length=output_length)
        ## Exits loop as soon as we reach the end of the dataset
        if len(yi) < output_length:
            break
        X.append(Xi)
        y.append(yi)

    X = np.array(X)
    y = np.array(y)
    y = np.squeeze(y)

    if shuffle:
        idx = np.arange(len(X))
        np.random.shuffle(idx)
        X = X[idx]
        y = y[idx]

    print("Split-set shape:")
    print(f"X: {X.shape}, y: {y.shape}")

    return X, y

def plot_history(history):
    '''
    PLots the loss & metrics evolution for all epochs, for the training set & the validation set
    '''

    fig, ax = plt.subplots(1,2, figsize=(20,7))

    # --- LOSS: Sparse_categorical_crossentropy ---
    ax[0].plot(history.history['loss'])
    ax[0].plot(history.history['val_loss'])
    ax[0].set_title('Loss')
    ax[0].set_ylabel('Loss')
    ax[0].set_xlabel('Epoch')
    ax[0].legend(['Train', 'Validation'], loc='best')
    ax[0].grid(axis="x",linewidth=0.5)
    ax[0].grid(axis="y",linewidth=0.5)

    # --- METRICS: accuracy ---
    ax[1].plot(history.history['accuracy'])
    ax[1].plot(history.history['val_accuracy'])
    ax[1].set_title('accuracy')
    ax[1].set_ylabel('accuracy')
    ax[1].set_xlabel('Epoch')
    ax[1].legend(['Train', 'Validation'], loc='best')
    ax[1].grid(axis="x",linewidth=0.5)
    ax[1].grid(axis="y",linewidth=0.5)

    return ax

# Cross-validate the model
def cross_validate(df: pd.DataFrame):
    '''
    Argument : the dataframe on which to input the model

    Cross-validate the model into a number of folds defined by the FOLD_LENGTH, FOLD_STRIDE & STRIDE defined, returns the mean accuracy for all the folds
    '''

    list_of_accuracy_baseline_model = []
    list_of_accuracy_recurrent_model = []

    # 1 - Creating FOLDS
    # =======================================================

    folds = get_folds(df, FOLD_LENGTH, FOLD_STRIDE)

    for fold_id, fold in enumerate(folds):

        print('=' * 50)
        print(f"Fold n°{fold_id+1}")
        print('=' * 50)

        # 2 - CHRONOLOGICAL TRAIN TEST SPLIT of the current FOLD
        # =======================================================

        (fold_train, fold_test) = train_test_split(fold = fold,
                                                train_test_ratio = TRAIN_TEST_RATIO,
                                                input_length = INPUT_LENGTH,
                                                horizon = HORIZON)

        # 3 - Scanninng fold_train and fold_test for SEQUENCES
        # =======================================================

        X_train, y_train = get_X_y(fold = fold_train,
                                horizon = HORIZON,
                                input_length = INPUT_LENGTH,
                                output_length = OUTPUT_LENGTH,
                                stride = STRIDE)

        X_test, y_test = get_X_y(fold = fold_test,
                                horizon = HORIZON,
                                input_length = INPUT_LENGTH,
                                output_length = OUTPUT_LENGTH,
                                stride = STRIDE)

        # 4.1 - Baseline Model
        # =======================================================
        df, accuracy_baseline = baseline(df)

        list_of_accuracy_baseline_model.append(accuracy_baseline)

        print("-"*50)

        # 4.2 - Model
        # =======================================================

        # Initializing the model
        model = init_model(X_train)

        # Compiling the model
        compile_model(model)

        # Training
        model, history = fit_model(model, X_train, y_train)
        plot_history(history)
        plt.show()

        # Evaluation
        res = evaluate_model(model, X_test, y_test)
        accuracy_lstm = res[1]

        list_of_accuracy_recurrent_model.append(accuracy_lstm)

        print("\n")
        print(f"Accuracy baseline fold n°{fold_id+1} = {round(accuracy_baseline, 2)}")
        print(f"Accuracy LSTM fold n°{fold_id+1} = {round(accuracy_lstm, 2)}")

        # 4.3 - Comparison model vs baseline for the current fold
        # =======================================================
        print(f"🏋🏽‍♂️ Improvement/Decrease vs. Baseline: {round(((accuracy_lstm-accuracy_baseline)/accuracy_baseline)*100,2)} % \n")

    cv_accuracy_baseline = np.mean(list_of_accuracy_baseline_model)
    cv_accuracy_lstm = np.mean(list_of_accuracy_recurrent_model)

    print("="*50)
    print("Result for all folds")
    print(f"Average accuracy baseline = {round(cv_accuracy_baseline, 2)}")
    print(f"Average accuracy LSTM = {round(cv_accuracy_lstm, 2)}")
    print(f"🏋🏽‍♂️ Improvement/Decrease vs. Baseline: {round(((cv_accuracy_lstm-cv_accuracy_baseline)/cv_accuracy_baseline)*100,2)} % \n")
