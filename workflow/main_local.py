# Main python file containing all the workflow, by importing modules from other python files

 # Imports
import pandas as pd
from workflow.params import LOCAL_DATA_PATH,LOCAL_DATA_PATH_2, FOLD_LENGTH, FOLD_STRIDE, STRIDE, TRAIN_TEST_RATIO, N_FEATURES, INPUT_LENGTH, TARGET, TARGET_COLUMN_IDX, N_TARGETS, OUTPUT_LENGTH, HORIZON
from workflow.preprocessing import preprocess
from workflow.model import init_model, compile_model, fit_model, evaluate_model, predict
from workflow.model_evaluation import train_test_split, get_X_y, cross_validate
from workflow.registry import save_model
from workflow.registry import load_model

# # Load data
# raw_df = pd.read_csv(f"{LOCAL_DATA_PATH}.csv").copy()

# # Preprocess raw data
# df = preprocess(raw_df)

# # Count the number of classes for the target
# df[TARGET].value_counts()

# # Cross validate (to delete from main.py at the end)
# cross_validate(df)

# # Train-test split
# (df_train, df_test) = train_test_split(fold = df,
#                                         train_test_ratio = TRAIN_TEST_RATIO,
#                                         input_length = INPUT_LENGTH,
#                                         horizon = HORIZON)

# #X_train, y_train = get_X_y(fold = df_train,
#                         horizon = HORIZON,
#                         input_length = INPUT_LENGTH,
#                         output_length = OUTPUT_LENGTH,
#                         stride = STRIDE)

# #X_test, y_test = get_X_y(fold = df_test,
#                         horizon = HORIZON,
#                         input_length = INPUT_LENGTH,
#                         output_length = OUTPUT_LENGTH,
#                         stride = STRIDE)

# # Model initiation & compiling
# #model = init_model(X_train, y_train)
# #compile_model(model)

# # Model training
# #model, history = fit_model(model, X_train, y_train)

# #Model save
# #save_model(model)

# # Model evaluation
# #res = evaluate_model(model, X_test, y_test)
# #res

# Model prediction
#y_true = df[TARGET]
#y_pred = predict(model, X_test)

#y_pred[-1]

#Old
#if __name__ == '__main__':
#    preprocess(raw_df)
#    cross_validate()
#    train_test_split(fold = df,
#                     train_test_ratio = TRAIN_TEST_RATIO,
#                     input_length = INPUT_LENGTH,
#                     horizon = HORIZON)
#    get_X_y(fold = df_train,
#            horizon = HORIZON,
#            input_length = INPUT_LENGTH,
#            output_length = OUTPUT_LENGTH,
#            stride = STRIDE)
#    init_model(X_train, y_train))
#    compile_model(model)
#    fit_model(model, X_train, y_train)
#    save_model(model)
#    evaluate_model(model, X_test, y_test)
#    predict(model, X_test)

if __name__ == '__main__':

    raw_df = pd.read_csv(f"{LOCAL_DATA_PATH_2}.csv").copy()

    df = preprocess(raw_df)

    (df_train, df_test)=train_test_split(fold = df,
                    train_test_ratio = TRAIN_TEST_RATIO,
                    input_length = INPUT_LENGTH,
                     horizon = HORIZON)

    X_train, y_train = get_X_y(fold = df_train,
                        horizon = HORIZON,
                        input_length = INPUT_LENGTH,
                        output_length = OUTPUT_LENGTH,
                        stride = STRIDE)

    X_test, y_test = get_X_y(fold = df_test,
                        horizon = HORIZON,
                        input_length = INPUT_LENGTH,
                        output_length = OUTPUT_LENGTH,
                        stride = STRIDE)

    model = init_model(X_train, y_train)

    model = compile_model(model)

    model, history = fit_model(model, X_train, y_train)

    save_model(model)

    model = load_model()

    metrics= evaluate_model(model[0], X_test, y_test)

    y_pred = predict(model[0], X_test)
