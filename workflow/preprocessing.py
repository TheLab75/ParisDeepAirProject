# Python file containing all the code for data preprocessing

# Imports de base
import pandas as pd
import numpy as np

from workflow.calcul_ATMO import pollution_peak_PM25, ATMO_encoder
from workflow.utils import covid_time

def preprocess(df):
    """Fonction de preprocessing qui va fonctionner en plusieurs étapes:
    1 - On utilise un simple imputer avec la stratégie median pour remplacer les NaN
    2 - On passe d'un format horaire à un format journalier
    3 - On calcule l'indice ATMO en utilisant un encoder homemade
    4 - Passage dans un robust scaler
    5 -
    """

    # Pour le moment on ne fait que sur la station du 16ème

    # Suppression des journées du 14/11/2022 et du 15/11/2022 (car incomplètes)
    df = df[:-25]

    # Drop des colonnes avec trop de NaN (plus de 30%)
    # A généraliser
    df = df.drop(columns=['O3', 'SO2', 'Station_name', 'Station_type'])

    # Call & application de l'imputer (sur X & y)
    from workflow.pipe import preprocessor_imputer

    df_preprocessed = pd.DataFrame(preprocessor_imputer.fit_transform(df))
    df_preprocessed = df_preprocessed.rename(columns={0:"PM25",1:"PM10",2:"NO2"})
    df_preprocessed = df_preprocessed.set_index(df['Date_time'])

    # Passage d'un format horaire à un format journalier avec la fonction du fichier daily basis (sur X & y)
    from workflow.daily_basis import mean_max_categorical

    df_daily = mean_max_categorical(df_preprocessed)

    #Calcul de l'ATMO (y)
    from workflow.calcul_ATMO import general_categorical
    from workflow.calcul_ATMO import calcul_ATMO

    df_daily_cat = df_daily.copy()
    df_daily_cat = general_categorical(df_daily_cat)
    df_daily_cat = calcul_ATMO(df_daily_cat)

    #Réduction de nombre de classes
    df_daily_cat['ATMO'] = df_daily_cat['ATMO'].apply(ATMO_encoder)

    #Création d'un dataframe y pour stocker notre indice ATMO (y)
    y = df_daily_cat[['Date_time','ATMO']]
    y.set_index(y['Date_time'],inplace=True)
    y = y[['ATMO']]

    #Création d'un dataframe X (X)
    X = df_daily.copy()
    X.set_index(X['Date_time'],inplace=True)
    X = X.drop(columns='Date_time')

    #Call & application du robust scaler sur les valeurs continues des polluants de X (X)
    from workflow.pipe import preprocessor_scaler

    X = pd.DataFrame(preprocessor_scaler.fit_transform(X))
    X = X.rename(columns={0:"PM25",1:"PM10",2:"NO2"})
    X = X.set_index(df_daily_cat['Date_time'])

    #Concat de X et Y en un seul dataframe
    df_concat = pd.concat([X, y], axis = 1)

    #Faire une f-string pour automatiser
    # df_concat.to_csv('../../data/pollution/inputs/Xy_PA75016.csv', index=True)

    #Reset de l'index pour le cyclical engineering
    df_concat = df_concat.reset_index()

    #Passage en date time puis création de deux colonnes : 1 pour le mois et 1 pour les jours de la semaine
    df_concat["Date_time"]= pd.to_datetime(df_concat["Date_time"])
    df_concat["day"] = df_concat["Date_time"].dt.day_of_week
    df_concat["month"] = df_concat["Date_time"].dt.month

    #Cyclical engineering pour les mois avec une création de deux colonnes
    months_in_a_year = 12

    df_concat['sin_Month'] = np.sin(2*np.pi*(df_concat.month-1)/months_in_a_year)
    df_concat['cos_Month'] = np.cos(2*np.pi*(df_concat.month-1)/months_in_a_year)

    #Cyclical engineering pour les jours de la semaine
    days_in_a_week = 7

    df_concat['sin_day'] = np.sin(2*np.pi*(df_concat.day-1)/days_in_a_week)
    df_concat['cos_day'] = np.cos(2*np.pi*(df_concat.day-1)/days_in_a_week)

    #Création d'une colonne qui prend en compte le covid
    df_concat["confinement"] = df_concat["Date_time"].copy()

    #Application de la fonction covidtime qui va indiquer de façon binaire les périodes de Covid
    df_concat["confinement"]=  df_concat["confinement"].apply(covid_time)

    # Ajout d'une feature permettant de capturer les périodes de pics extreme du PM2.5
    df_concat["Pollution_peak"] = df_concat["PM25"]
    df_concat["Pollution_peak"] = df_concat["Pollution_peak"].apply(pollution_peak_PM25)
    df_concat = df_concat.drop(columns=['day'])
    df_concat = df_concat.drop(columns=['month'])
    df_concat = df_concat.set_index(df_concat['Date_time'])
    df_concat = df_concat.drop(columns=['Date_time'])

    #Faire une f-string pour exporter en .csv le dataframe concaténé
    df_concat.to_csv('../../data/pollution/inputs/Xy_PA75016.csv', index=True)

    return df_concat
