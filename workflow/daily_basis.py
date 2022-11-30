# Python file containing all the code to convert datasets from an hourly-basis to a daily-basis

def mean_max_categorial(df):
    """Function that returns the daily average of "PM25", "PM10" and the daily maximum of "NO2"
    """
    #Parler du problème concernant l'utilisation de cette fonction vu qu'on va avoir des combinaisons de polluants différentes
    # pour chaque station
    #if df.columns

    df["PM25_mean"] = df.groupby(['Date_time'])["PM25"].mean()
    df["PM10_mean"] = df.groupby(['Date_time'])["PM10"].mean()
    df["NO2_max"] = df.groupby(['Date_time'])["NO2"].max()

    return df
