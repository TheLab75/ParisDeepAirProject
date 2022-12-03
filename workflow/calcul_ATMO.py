# Python file containing all the code to calculate the daily ATMO index (y in our model)

def general_categorical(df):

    '''Function that creates a new colum for each pollutant and encodes the continuous value of the pollutant into one of the 6 classes
    From 0 to 5'''

    List_polluant = ["PM25","PM10","NO2","O3","SO2"]
    # List_PM25 =[]
    # List_PM10 = []
    # List_N02 = []
    # List_O3 =[]
    # List_S02 = []

    for element in df.columns:

        if element == List_polluant[0]:
            df['PM25_categorical'] = df.PM25.apply(PM25_categorical)

        elif element == List_polluant[1]:
            df['PM10_categorical'] = df.PM10.apply(PM10_categorical)

        elif element == List_polluant[2]:
            df['NO2_categorical'] = df.NO2.apply(NO2_categorical)

        elif element == List_polluant[3]:
            df['O3_categorical'] = df.O3.apply(O3_categorical)

        elif element == List_polluant[4]:
            df['SO2_categorical'] = df.SO2.apply(SO2_categorical)

    return df

# A mettre à jour ou à supprimer ?
def general_ATM0():

    List_categorical = ["PM25_categorical","PM10_categorical","NO2_categorical","O3_categorical","SO2_categorical"]

    #on veut appliquer une fonction sur plusieurs élements
    #if

    df["general_Atmo"] = df.max(axis=1)

def PM25_categorical(x):

    """Function that categorizes the pollutant PM 2.5 into one of the 5 classes in function of the ATMO index
    Class 0 => from 0 to 10
    Class 1 => from 10 to 20
    Class 2 => from 20 to 25
    Class 3 => from 25 to 50
    Class 4 => from 50 to 75
    Class 5 => from 75 to ∞
    """

    if 10>x>=0:
        return 0

    elif 20>x>=10:
        return 1

    elif 25>x>=20:
        return 2

    elif 50>x>=25:
        return 3

    elif 75>x>=50:
        return 4

    elif x>75:
        return 5


def PM10_categorical(x):

    """Function that categorizes the pollutant PM 10 into one of the 5 classes in function of the ATMO index
    Class 0 => from 0 to 20
    Class 1 => from 20 to 40
    Class 2 => from 40 to 50
    Class 3 => from 50 to 100
    Class 4 => from 100 to 150
    Class 5 => from 150 to ∞
    """

    if 20>x>=0:
        return 0

    elif 40>x>=20:
        return 1

    elif 50>x>=40:
        return 2

    elif 100>x>=50:
        return 3

    elif 150>x>=100:
        return 4

    elif x>=150:
        return 5

def NO2_categorical(x):

    """Function that categorizes the pollutant "Dioxyde d'Azote" (NO2) into one of the 5 classes in function of the ATMO index
    Class 0 => from 0 to 40
    Class 1 => from 40 to 90
    Class 2 => from 90 to 120
    Class 3 => from 120 to 230
    Class 4 => from 230 to 340
    Class 5 => from 340 to ∞
    """

    if 40>x>=0:
        return 0

    elif 90>x>=40:
        return 1

    elif 120>x>=90:
        return 2

    elif 230>x>=120:
        return 3

    elif 340>x>=230:
        return 4

    elif x>=340:
        return 5

def O3_categorical(x):

    """Function that categorizes the pollutant Ozone (03) into one of the 5 classes in function of the ATMO index
    Class 0 => from 0 to 50
    Class 1 => from 50 to 100
    Class 2 => from 100 to 130
    Class 3 => from 130 to 240
    Class 4 => from 240 to 380
    Class 5 => from 380 to ∞
    """

    if 50>x>=0:
        return 0

    elif 100>x>=50:
        return 1

    elif 130>x>=100:
        return 2

    elif 240>x>=130:
        return 3

    elif 380>x>=240:
        return 4

    elif x>=380:
        return 5


def SO2_categorical(x):

    """Function that categorizes the pollutant "Dioxyde de Souffre" (SO2) into one of the 5 classes in function of the ATMO index
    Class 0 => from 0 to 100
    Class 1 => from 100 to 200
    Class 2 => from 200 to 350
    Class 3 => from 350 to 500
    Class 4 => from 500 to 750
    Class 5 => from 750 to ∞
    """

    if 100>x>=0:
        return 0

    elif 200>x>=100:
        return 1

    elif 350>x>=200:
        return 2

    elif 500>x>=350:
        return 3

    elif 750>x>=500:
        return 4

    elif x>=750:
        return 5

def calcul_ATMO(df):

    """Function that calculates the ATMO level
    """
    #Fonction spécifique à la station du 16ème
    #Qui fait le max entre PM10, PM25, NO2 et SO2

    df["ATMO"] = df[["PM10_categorical", "PM25_categorical", "NO2_categorical"]].max(axis=1)

    return df

def pollution_peak_PM25(x):

    '''
    Permet d'identifier les pics de pollution selon le PM25
    '''

    if x > 80:
        return 1
    else:
        return 0

def ATMO_encoder(x):

    '''
    Permet de réduire le nombre de catégories de l'ATMO de 5 à 3.
    Classe 3 : anciennes classes 0 (bon), 1 (moyen), 2 (dégradé), 3 (mauvais)
    Classe 4 : ancienne classe 4 (très mauvais)
    Classe 5 : ancienne classe 5 (extrêmement mauvais)
    '''

    if x == 0:
        return 0

    elif  x == 1:
        return 0

    elif x== 2:
        return 0

    elif x == 3:
        return 0

    elif x == 4:
        return 1

    else:
        return 2
