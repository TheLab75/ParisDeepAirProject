# Python file containing all the code to convert datasets from an hourly-basis to a daily-basis
import pandas as pd

def mean_max_categorial(df):
    """Function that returns the daily average of "PM25", "PM10" and the daily maximum of "NO2"
    """
    #Parler du problème concernant l'utilisation de cette fonction vu qu'on va avoir des combinaisons de polluants différentes
    # pour chaque station
    #if df.columns

    #Convertir la colonne Date_time en date
    df = df.reset_index()
    df['Date_time'] = df['Date_time'].astype(str).str[0:10]

    #Ici on groupby par date pour les colonnes liées aux particules qui sont calculées en réalisant une moyenne journalière
    df_pm = df.groupby(['Date_time'])[["PM25", "PM10"]].mean().round(2)

    #Ici on groupby par date pour les colonnes liées au NO2, calculé en réalisant un max journalier
    df_pollu = df.groupby(by="Date_time")['NO2'].max().round(2)

    #Ici on merge les deux dataframes créées pour en faire un seul
    df_merged = pd.merge(df_pm,df_pollu,on="Date_time")
    df_merged = df_merged.reset_index()

    return df_merged
