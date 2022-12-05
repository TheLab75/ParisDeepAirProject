from datetime import datetime
import pandas as pd

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware



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

from workflow.model import predict
@app.get("/predict")
def predict_1(X_test):

    y_pred = predict(X_test)

    return dict(prédiction=(y_pred))


from workflow.data_viz import plot_pollutant_v1
from workflow.data_viz import plot_pollutant_v2
from workflow.data_viz import weekday_pollutant
from workflow.data_viz import plot_shift_pollutant

@app.get("/data_viz")
def data_viz(df,pollutant,period,choice_of_plot,year):
    #On doit faire choisir à l'utilisateur la station
    #Puis lui montrer dans une liste déroulante, les polluants disponibles

    if choice_of_plot == "All in one graph":
        plot = plot_pollutant_v1(df,pollutant,period)

    elif choice_of_plot == "1 graph for one year":
        plot = plot_pollutant_v2(df,pollutant,period)

    elif choice_of_plot == " Week day":
        plot = weekday_pollutant(df,pollutant)

    elif choice_of_plot == "Shifting":
        #on doit faire sélectionenr à l'utilisateur une année afin de plot l'année sélectionnée
        plot = plot_shift_pollutant(df,year)


    return dict(plot_1 = plot)
