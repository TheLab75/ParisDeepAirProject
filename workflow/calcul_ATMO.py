
def PM25_categorical(x):
    """Function that categorizes the pollutant PM 2.5 into one of the 5 classes in function of the ATMO index
    Class 0 => from 0 to 10
    Class 1 => from 10 to 20
    Class 2 => from 20 to 25
    Class 3 => from 25 to 50
    Class 4 => from 50 to 75
    Class 5 => from 75 to ∞
    """

    if 10>x>0:
        return 0

    elif 20>x>10:
        return 1

    elif 25>x>20:
        return 2

    elif 50>x>25:
        return 3

    elif 75>x>50:
        return 4
    elif 75<x:
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
    if 20>x>0:
        return 0

    elif 40>x>20:
        return 1

    elif 50>x>40:
        return 2

    elif 100>x>50:
        return 3

    elif 150>x>100:
        return 4

    elif 150<x:
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
    if 40>x>0:
        return 0

    elif 40>x>90:
        return 1

    elif 90>x>120:
        return 2

    elif 120>x>230:
        return 3

    elif 230>x>340:
        return 4

    elif 340<x:
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
    if 50>x>0:
        return 0

    elif 50>x>100:
        return 1

    elif 100>x>130:
        return 2

    elif 130>x>240:
        return 3

    elif 240>x>380:
        return 4

    elif 380<x:
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

    if 100>x>0:
        return 0

    elif 200>x>100:
        return 1

    elif 350>x>200:
        return 2

    elif 500>x>350:
        return 3

    elif 750>x>500:
        return 4

    elif 750<x:
        return 5


def calcul_ATMO(df):
    """Function that calculates the ATMO level
    """
    #Parler du problème concernant l'utilisation de cette fonction vu qu'on va avoir des combinaisons de polluants différentes
    # pour chaque station
    #if df.columns

    df["ATMO"] = df[["PM10_categorical", "PM25_categorical", "NO2_categorical", "O3_categorical","SO2_categorical"]].max()


    return df.ATMO
