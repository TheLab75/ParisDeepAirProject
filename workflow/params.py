# Python file centralizing all the parameters


import os

#Data path
LOCAL_DATA_PATH = "../data/pollution/2_Processed/PA75016"
LOCAL_DATA_PATH_2 = "data/pollution/2_Processed/PA75016"
LOCAL_DATA_PATH_3 = 'data/pollution/'


# LOCAL_DATA_PATH = os.path.join(os.path.expanduser(‘~’), “.lewagon”, “mlops”, “data”)
# LOCAL_REGISTRY_PATH =  os.path.join(os.path.expanduser(‘~’), “.lewagon”, “mlops”, “training_outputs”)



# Model params
# Folds
FOLD_LENGTH = 521 # dont 365J Train +  156J Test
FOLD_STRIDE = int(209) # sliding each semester - décalage de 209J pour obtenir 7 folds
STRIDE = 1 # sliding every  days, for subfolds

# Temporal Train-Test split
TRAIN_TEST_RATIO = 0.7 #70% de train et 30% de test par fold

# Inputs
N_FEATURES = 4  # 3 polluants + l'ATMO index
INPUT_LENGTH = 7 # - Records 1 week ~ 7 days. One week is quite common for air quality

# Outputs
TARGET = ['ATMO']
TARGET_COLUMN_IDX = 3 # Corresponds to the third column of the df
N_TARGETS = 1
OUTPUT_LENGTH = N_TARGETS*7 # Predicting one target, the ATMO index for 7 days

# Additional parameters
HORIZON = 1 # - You want to predict this point HORIZON = 1 day after the last known value

# Train parameters
batch_size = 32
epochs = 200
patience = 5
