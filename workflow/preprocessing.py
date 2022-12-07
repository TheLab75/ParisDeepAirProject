# Python file containing all the code for data preprocessing

# Imports de base
import pandas as pd
import numpy as np

from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler

from workflow.daily_basis import mean_max_categorical
from workflow.calcul_ATMO import general_categorical
#from workflow.calcul_ATMO import calcul_ATMO
from workflow.calcul_ATMO import general_ATM0

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

    # Suppression des journées des J-1 et J-2 (car incomplètes)
    df = df[:-25]

    # Suppression des colonnes station name & station type
    #df = df.drop(columns=['Station_name', 'Station_type'])

    # Généralisation du drop des colonnes avec trop de NaN (plus de 30%)
    for element in df.columns:
        NA_percent = df[element].isna().sum()/len(df) * 100
        if NA_percent > 30:
            df = df.drop(columns=element)
            print(f"You have dropped {element} with {round(NA_percent,2)}% of NA")

    # A généraliser
    #df = df.drop(columns=['O3', 'SO2', 'Station_name', 'Station_type'])

    # Call & application de l'imputer (sur X & y)
    liste_polluant= ["PM25","PM10","NO2","O3","SO2"]
    num_features=[]

    for element in df.columns:
        if element in liste_polluant:
            num_features.append(element)

    num_imputer_normal = make_pipeline(
        SimpleImputer(strategy='median'))

    preprocessor_imputer = make_column_transformer(
        (num_imputer_normal, num_features))

    df_preprocessed = pd.DataFrame(preprocessor_imputer.fit_transform(df))

    #df_preprocessed = df_preprocessed.rename(columns={0:"PM25",1:"PM10",2:"NO2"})
    #=> On généralise

    # Vu que Louis a, au préalable classer les polluants de chaque station se l'ordre suivant : ["PM25","PM10","NO2","O3","SO2"]
    sorted_list_polluant = []
    for element in df.columns:
        if element in liste_polluant:
            sorted_list_polluant.append(element)

    # On doit faire une condition avec la taille de la liste des polluants présents dans le df
    if len(sorted_list_polluant) == 1:
        df_preprocessed = df_preprocessed.rename(columns={0:sorted_list_polluant[0]})

    elif len(sorted_list_polluant) == 2:
        df_preprocessed = df_preprocessed.rename(columns={0:sorted_list_polluant[0],
                                                        1:sorted_list_polluant[1]})

    elif len(sorted_list_polluant) == 3:
        df_preprocessed = df_preprocessed.rename(columns={0:sorted_list_polluant[0],
                                                        1:sorted_list_polluant[1],
                                                        2:sorted_list_polluant[2]})

    elif len(sorted_list_polluant) == 4:
        df_preprocessed = df_preprocessed.rename(columns={0:sorted_list_polluant[0],
                                                        1:sorted_list_polluant[1],
                                                        2:sorted_list_polluant[2],
                                                        3:sorted_list_polluant[3]})

    elif len(sorted_list_polluant) == 5:
        df_preprocessed = df_preprocessed.rename(columns={0:sorted_list_polluant[0],
                                                        1:sorted_list_polluant[1],
                                                        2:sorted_list_polluant[2],
                                                        3:sorted_list_polluant[3],
                                                        4:sorted_list_polluant[4]})

    df_preprocessed = df_preprocessed.set_index(df['Date_time'])

    # Passage d'un format horaire à un format journalier avec la fonction du fichier daily basis (sur X & y)
    df_daily = mean_max_categorical(df_preprocessed)

    #Calcul de l'ATMO (y)
    df_daily_cat = df_daily.copy()
    df_daily_cat = general_categorical(df_daily_cat)
    #df_daily_cat = calcul_ATMO(df_daily_cat)
    df_daily_cat = general_ATM0(df_daily_cat)

    #Réduction de nombre de classes
    #0 => Classes 0, 1
    #1 => Classes 2, 3, 4, 5
    df_daily_cat['ATMO'] = df_daily_cat['ATMO'].apply(ATMO_encoder)

    #Création d'un dataframe y pour stocker notre indice ATMO (y)
    y = df_daily_cat[['Date_time','ATMO']]
    y.set_index(y['Date_time'],inplace=True)
    y = y[['ATMO']]

    #Création d'un dataframe X (X)
    X = df_daily.copy()
    X.set_index(X['Date_time'],inplace=True)
    X = X.drop(columns='Date_time')

    # Ajout d'une feature permettant de capturer les périodes de pics extreme du PM2.5
    # Cependant chaque station ne mesure pas les particules 2.5, il faut réussir à généraliser ce truc,
    # soit on fait un % de plus par rapport à la valeur de la dernière classe pour chaque polluant genre 10% de plus
    if "PM25" in X.columns:
        X["Pollution_peak"] = X["PM25"]
        X["Pollution_peak"] = X["Pollution_peak"].apply(pollution_peak_PM25)

    # Code du scaler, à activer si modèle régression ou classification, à désactiver si Facebook prophet
    # #Call & application du robust scaler sur les valeurs continues des polluants de X (X)
    # preprocessor_scaler = make_pipeline(
    # RobustScaler())

    # X = pd.DataFrame(preprocessor_scaler.fit_transform(X))

    # #X = X.rename(columns={0:"PM25",1:"PM10",2:"NO2"})

    # if len(sorted_list_polluant) == 1:
    #     X = X.rename(columns={0:sorted_list_polluant[0]})

    # elif len(sorted_list_polluant) == 2:
    #     X = X.rename(columns={0:sorted_list_polluant[0],
    #                           1:sorted_list_polluant[1]})

    # elif len(sorted_list_polluant) == 3:
    #     X = X.rename(columns={0:sorted_list_polluant[0],
    #                           1:sorted_list_polluant[1],
    #                           2:sorted_list_polluant[2]})

    # elif len(sorted_list_polluant) == 4:
    #     X = X.rename(columns={0:sorted_list_polluant[0],
    #                           1:sorted_list_polluant[1],
    #                           2:sorted_list_polluant[2],
    #                           3:sorted_list_polluant[3]})

    # elif len(sorted_list_polluant) == 5:
    #     X = X.rename(columns={0:sorted_list_polluant[0],
    #                           1:sorted_list_polluant[1],
    #                           2:sorted_list_polluant[2],
    #                           3:sorted_list_polluant[3],
    #                           4:sorted_list_polluant[4]})

    # X = X.set_index(df_daily_cat['Date_time'])

    # col_list = list(X.columns)
    # print(col_list)
    # col_list[-1] = "Pollution_peak"
    # X.columns = col_list

    #Concat de X et Y en un seul dataframe
    df_concat = pd.concat([X, y], axis = 1)

    #Faire une f-string pour automatiser
    # df_concat.to_csv('../../data/pollution/inputs/Xy_PA75016.csv', index=True)

    #Récupération de la colonne "Date_time" en faisant reset de l'index pour le cyclical engineering
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

    df_concat = df_concat.drop(columns=['day'])
    df_concat = df_concat.drop(columns=['month'])
    df_concat = df_concat.set_index(df_concat['Date_time'])
    df_concat = df_concat.drop(columns=['Date_time'])

    #Faire une f-string pour exporter en .csv le dataframe concaténé
    #df_concat.to_csv('../../data/pollution/inputs/Xy_PA75016.csv', index=True)

    print("DataFrame is processed, you can play with it !")

    return df_concat

def preprocess_without_scaling(df):
    """
    Fonction utilisée pour preprocesser une station sans la scaler afin de pouvoir faire de la data viz sur cette station
    """

    df = df[:-25]
    df = df.drop(columns=['Station_name', 'Station_type'])

    # Généralisation du drop des colonnes avec trop de NaN (plus de 30%)
    for element in df.columns:
        NA_percent = df[element].isna().sum()/len(df) * 100
        if NA_percent > 30:
            df = df.drop(columns=element)
            print(f"You have dropped {element} with {round(NA_percent,2)}% of NA")

    # A généraliser
    #df = df.drop(columns=['O3', 'SO2', 'Station_name', 'Station_type'])

    # Call & application de l'imputer (sur X & y)
    liste_polluant= ["PM25","PM10","NO2","O3","SO2"]
    num_features=[]

    for element in df.columns:
        if element in liste_polluant:
            num_features.append(element)

    #df = df.set_index(df['Date_time'])

    num_imputer_normal = make_pipeline(
        SimpleImputer(strategy='median'))

    preprocessor_imputer = make_column_transformer(
        (num_imputer_normal, num_features))

    df_preprocessed = pd.DataFrame(preprocessor_imputer.fit_transform(df))

    sorted_list_polluant = []
    for element in df.columns:
        if element in liste_polluant:
            sorted_list_polluant.append(element)

    # On doit faire une condition avec la taille de la liste des polluants présents dans le df
    if len(sorted_list_polluant) == 1:
        df_preprocessed = df_preprocessed.rename(columns={0:sorted_list_polluant[0]})

    elif len(sorted_list_polluant) == 2:
        df_preprocessed = df_preprocessed.rename(columns={0:sorted_list_polluant[0],
                                                        1:sorted_list_polluant[1]})

    elif len(sorted_list_polluant) == 3:
        df_preprocessed = df_preprocessed.rename(columns={0:sorted_list_polluant[0],
                                                        1:sorted_list_polluant[1],
                                                        2:sorted_list_polluant[2]})

    elif len(sorted_list_polluant) == 4:
        df_preprocessed = df_preprocessed.rename(columns={0:sorted_list_polluant[0],
                                                        1:sorted_list_polluant[1],
                                                        2:sorted_list_polluant[2],
                                                        3:sorted_list_polluant[3]})

    elif len(sorted_list_polluant) == 5:
        df_preprocessed = df_preprocessed.rename(columns={0:sorted_list_polluant[0],
                                                        1:sorted_list_polluant[1],
                                                        2:sorted_list_polluant[2],
                                                        3:sorted_list_polluant[3],
                                                        4:sorted_list_polluant[4]})

    df_preprocessed = df_preprocessed.set_index(df['Date_time'])

    # Passage d'un format horaire à un format journalier avec la fonction du fichier daily basis (sur X & y)
    df_daily = mean_max_categorical(df_preprocessed)

    #Calcul de l'ATMO (y)
    df_daily_cat = df_daily.copy()

    df_daily_cat = general_categorical(df_daily_cat)

    df_daily_cat = general_ATM0(df_daily_cat)

    #Réduction de nombre de classes
    #0 => Classes 0, 1
    #1 => Classes 2, 3, 4, 5
    df_daily_cat['ATMO'] = df_daily_cat['ATMO'].apply(ATMO_encoder)

    #Création d'un dataframe y pour stocker notre indice ATMO (y)
    y = df_daily_cat[['Date_time','ATMO']]
    y.set_index(y['Date_time'],inplace=True)
    y = y[['ATMO']]

    #Création d'un dataframe X (X)
    X = df_daily.copy()
    X.set_index(X['Date_time'],inplace=True)
    X = X.drop(columns='Date_time')

    #Concat de X et Y en un seul dataframe
    df_concat = pd.concat([X, y], axis = 1)

    #Reset de l'index pour avoir le Date_time en colonne et pas en index
    #Voir pourquoi le reset_index ne fonctionne pas sur la fonction preprocess without scaling
    df_concat = df_concat.reset_index()

    print(f"You have processed the dataframe without scaling it, now you can play with data viz functions " )

    return df_concat
