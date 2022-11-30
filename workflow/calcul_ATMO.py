# Python file containing all the code to calculate the daily ATMO index (y in our model)

def PM10_categorical(x):
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


def PM25_categorical(x):

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

def NO2_categorical(x):

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

def ATMO_categorial(x):
    data["ATMO"] = data[["PM10_categorical", "PM25_categorical", "NO2_categorical", "O3_categorical"]].max()


    return data.ATMO
