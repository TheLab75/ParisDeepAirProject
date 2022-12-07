from datetime import datetime
import pandas as pd

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from workflow.registry import predict,load_model,save_model
from workflow.preprocessing import preprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

#On va load le modèle pour que l'API soit plus réactive

#app.state.model = load_model()

@app.get("/")
def root():
    return dict(greeting="Hello Philippe le BOSS")

# app.state.model = load_model()
# test = load_model()
# #Ou est la variable de mon load model ?

# @app.get("/predict")
# # def model_predict(model = None, X_new=None):
# #     cluster_list=['Paris_est','Paris_south',
# #                    'Paris_north','Paris_west','Paris_center']

# #     X_preprocess = preprocess(X_new)
# #     result = {}
# #     if model != None:
# #         model_index = cluster_list.index(model)
# #         specific_model = app.state.model[model_index]
# #         result[model] = specific_model.predict(X_new)
# #     else:
# #         for i,v in enumerate(cluster_list):
# #             result[v]=app.state.model[i].predict(i,X_new)
# #     return result

app.state.model = load_model()

@app.get("/predict")
def predict_model(station=None):
    #On veut en argument notre liste qui sort du load_model()

    cluster_list=['Paris_est','Paris_south',
                   'Paris_north','Paris_west','Paris_center']
    models = app.state.model

    if not station or station== "All":
        return predict(models)

    return predict(models)[station]

    # la fonction predict prend comme argument le résultat de la fonction load_model
    prediction = predict(test)

    prediction = predict(test)

    for element in cluster_list:
        for pred in prediction:
            dico_pred[element] = pred

    # if model != None:
    #     model_index = cluster_list.index(model)
    #     specific_model = app.state.model[model_index]
    #     result[model] = specific_model.predict(X_new)
    # else:
    #     for i,v in enumerate(cluster_list):
    #         result[v]=app.state.model[i].predict(i,X_new)
    # return result

    return dico_pred
