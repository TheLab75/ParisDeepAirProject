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


@app.get("/")
def root():
    return dict(greeting="Hello Philippe le BOSS")


app.state.model = load_model()

@app.get("/predict")
def predict_model(station=None):

    cluster_list=['Paris_east','Paris_south',
                   'Paris_north','Paris_west','Paris_center']

    models = app.state.model

    if not station or station== "All":
        return predict(models)

    return predict(models)[station]
