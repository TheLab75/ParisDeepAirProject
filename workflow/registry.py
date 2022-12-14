import glob
import os
import time
import pickle
import datetime
import pandas as pd
import plotly.express as px
from greykite.framework.templates.autogen.forecast_config import ForecastConfig, MetadataParam, ModelComponentsParam
from greykite.framework.benchmark.data_loader_ts import DataLoaderTS
from greykite.framework.templates.forecaster import Forecaster
import numpy as np
from pathlib import Path

cluster_list=['Paris_east','Paris_south','Paris_north','Paris_west','Paris_center']

# def save_model(forecaster) -> None:

#     for cluster in cluster_list:

#         # TODO : ATTENTION A MODIF
#         # Create the PATH directory if it does exist
#         # Path(PATH).mkdir(parents=True, exist_ok=True)
#         #model_path = os.path.join(PATH, "model_save",'models', cluster)

#         destination_dir = os.path.join(PATH,'model_save','models', cluster)

#         # Create the LOCAL_REGISTRY_PATH directory if it does exist
#         Path(LOCAL_REGISTRY_PATH).mkdir(parents=True, exist_ok=True)
#         #model_path = os.path.join(LOCAL_REGISTRY_PATH, "model_save",'models', cluster)

#         destination_dir = os.path.join(LOCAL_REGISTRY_PATH,'model_save','models',cluster)


#         forecaster.dump_forecast_result(
#             destination_dir,
#             object_name=cluster,
#             dump_design_info=True,
#             overwrite_exist_dir=True)
#         print(f"You have saved the model in {destination_dir}")

#     return None

def load_model(save_copy_locally=False):

    cluster_list_2 = ["cluster1_Ouest","cluster2_Nord","cluster3_Est","cluster4_Sud","cluster5_Centre"]
    list_model= []

    for cluster in cluster_list_2:
        source_dir = os.path.join("/code/ParisDeepAirProject/model_greykite",f"{cluster}")

        forecaster = Forecaster()
        forecaster.load_forecast_result(source_dir,load_design_info=True)
        result = forecaster.forecast_result
        list_model.append(result)

    # print(list_model)
    return list_model

def predict(list_model):

    list_prediction = []
    for element in list_model:

        df_predict_and_actual = element.forecast.df
        df_predict_and_actual = df_predict_and_actual[1:]
        seven_days_predicted = pd.DataFrame(np.round(df_predict_and_actual['forecast']).astype(int))[-7:] #remove 7 rows forecasts
        #seven_days_predicted = pd.DataFrame(np.round(df_predict_and_actual['forecast'],4))[-7:] #remove 7 rows forecasts
        #reset indef to get day as column

        seven_days_predicted.reset_index(inplace=True, drop=True) # get the good number for days
        seven_days_predicted.reset_index(inplace=True, drop=None) # put is as columns
        seven_days_predicted.columns = ['days', 'forecast'] # rename columns
        list_prediction.append(seven_days_predicted)

    my_dict = {}
    for i, predict in enumerate(list_prediction):
        my_dict[cluster_list[i]] = {f'day{i+1}': v for i, v in enumerate(predict['forecast'])}
# return dico_general
    return my_dict

if __name__ == '__main__':
    test = load_model()
    predict(test)
    pass
