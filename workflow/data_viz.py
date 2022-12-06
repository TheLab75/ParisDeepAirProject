#Imports de base
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

def data_viz(df):
    """Cette fonction nécessite comme un argument un dataframe préprocessed mais sans le scaling"""

#création des colonnes
    df["Date_time"]= pd.to_datetime(df["Date_time"])
    df["year"] = df["Date_time"].dt.year
    df["week"] = df["Date_time"].dt.week
    df["day"] = df["Date_time"].dt.day
    df["month"] = df["Date_time"].dt.month
    df["weekday_name"] = df["Date_time"].dt.day_of_week

    #Style à changer si on le souhaite
    #https://github.com/dhaitz/matplotlib-stylesheets
    plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

    ##Création d'un dataframe groupé par année et par semaine
    #df_all_week = df.groupby(by=["year","week"],as_index=False).mean()

    #Passage des jours de la semaine allant de 0 à 6 en Lundi jusque Dimanche
    #df_days = df.copy()
    #df_days['weekday_name'] = df_days['weekday_name'].apply(lambda x: calendar.day_name[x])

    #Shifting sur 7 jours
    #=> Création des colonnes de shifting sur 7 jours
    #if "PM25" in df.columns:
        # df["J-1"] = df["PM25"].shift(1)
        # df["J-2"] = df["PM25"].shift(2)
        # df["J-3"] = df["PM25"].shift(3)
        # df["J-4"] = df["PM25"].shift(4)
        # df["J-5"] = df["PM25"].shift(5)
        # df["J-6"] = df["PM25"].shift(6)
        # df["J-7"] = df["PM25"].shift(7)

    return df

def plot_pollutant_v1(df,pollutant,period):
    """ The DataFrame should be processed without scaling and passed within data_viz
    You just need to chosse a pollutant and a period of time ("month","week")
    The V1 is plotting every curves on the same graph
    """
    #Création d'un dataframe groupé par année et par la période indiquée en input
    df_groupby = df.groupby(by=["year",period],as_index=False).mean()

    #df_all_month = df.groupby(by=["year","month"],as_index=False).mean()

    if period == "month":

        #Passage des mois allant de 1 à 12 en Janvier à Décembre
        df_groupby['month'] = df_groupby['month'].apply(lambda x: calendar.month_abbr[x])

        plt.figure(figsize=(12,5))

        plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')


        ax1 = sns.lineplot(x = period, y = pollutant, data=df_groupby.iloc[:12],
                    marker = "o",label="2018")

        sns.lineplot(x = period, y = pollutant, data=df_groupby.iloc[12:24],
                    marker = "o",label="2019")

        sns.lineplot(x = period, y =pollutant, data=df_groupby.iloc[24:36],
                    marker = "o",label="2020")

        sns.lineplot(x = period, y = pollutant, data=df_groupby.iloc[36:48],
                    marker = "o",label="2021")

        sns.lineplot(x = period, y = pollutant, data=df_groupby.iloc[48:58],
                    marker = "o",label="2022").set_title(f"{pollutant} Mean per month per Year")

        # ax1.text("Apr",58,"1er Confinement",

        # fontsize = 7,          # Size
        # fontstyle = "italic",  # Style
        # color = "white",          # Color
        # ha = "center", # Horizontal alignment
        # va = "center") # Vertical alignment

        # ax1.text("Nov",58,"2ème Confinement",
        # fontsize = 7,          # Size
        # fontstyle = "italic",  # Style
        # color = "white",          # Color
        # ha = "center", # Horizontal alignment
        # va = "center") # Vertical alignment

        # ax1.text("May",58,"3ème Confinement",
        # fontsize = 7,          # Size
        # fontstyle = "italic",  # Style
        # color = "white",          # Color
        # ha = "center", # Horizontal alignment
        # va = "top") # Vertical alignment

    elif period == "week":
        plt.figure(figsize=(12,5))

        plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

        sns.lineplot(x = period, y = pollutant, data=df_groupby.iloc[:52],
                    marker = "o",label="2018")

        sns.lineplot(x = period, y = pollutant, data=df_groupby.iloc[53:104],
                    marker = "o",label="2019")

        sns.lineplot(x = period, y = pollutant, data=df_groupby.iloc[104:156],
                    marker = "o",label="2020")

        sns.lineplot(x = period, y = pollutant, data=df_groupby.iloc[156:208],
                    marker = "o",label="2021")

        sns.lineplot(x = period, y = pollutant, data=df_groupby.iloc[208:255],
                    marker = "o",label="2022").set_title(f"{pollutant} Mean per Week per Year")

    plt.show()

    return

def plot_pollutant_v2(df,pollutant,period):
    """ The DataFrame should be processed without scaling and passed within data_viz
    You just need to chosse a pollutant and a period of time ("month","week")
    The V1 is plotting one curve on one graph
    At the end, you will have one graph for each year
    """

    #Création d'un dataframe groupé par année et par la période indiquée par l'utilisateur
    df_groupby = df.groupby(by=["year",period],as_index=False).mean()

    if period == "month":

        #Passage des mois allant de 1 à 12 en Janvier à Décembre
        df_groupby['month'] = df_groupby['month'].apply(lambda x: calendar.month_abbr[x])
        fig, axes = plt.subplots(5, 1, figsize=(18, 18), sharey=True)
        fig.suptitle(f'MEAN {pollutant} per Month - Per Year')

        # 2018
        sns.lineplot(ax=axes[0], x = period, y = pollutant, data=df_groupby.iloc[:12],
                    marker = "o",label="2018",color = "green")
        #axes[0].set_title("2018")

        # 2019
        sns.lineplot(ax=axes[1],x = period, y = pollutant, data=df_groupby.iloc[12:24],
                    marker = "o",label="2019",color="b")
        #axes[1].set_title("2019")

        sns.lineplot(ax=axes[2],x = period, y = pollutant, data=df_groupby.iloc[24:36],
                    marker = "o",label="2020")
        #axes[2].set_title("2020")

        sns.lineplot(ax=axes[3],x = period, y = pollutant, data=df_groupby.iloc[36:48],
                    marker = "o",label="2021",color="r")

        #axes[3].set_title("2021")

        sns.lineplot(ax=axes[4],x = period, y = pollutant, data=df_groupby.iloc[48:58],
                    marker = "o",label="2022",color="orange")

        #axes[4].set_title("2022")

    elif period == "week":

            fig, axes = plt.subplots(5, 1, figsize=(18, 18), sharey=True)
            fig.suptitle(f'MEAN {pollutant} per week - Per Year')

             # 2018
            sns.lineplot(ax=axes[0],x = period, y = pollutant, data=df_groupby.iloc[:52],
                    marker = "o",label="2018",color = "green")
        #axes[0].set_ttle("2018")

        # 2019
            sns.lineplot(ax=axes[1],x = period, y = pollutant, data=df_groupby.iloc[53:104],
                    marker = "o",label="2019",color="b")
        #axes[1].set_title("2019")

        #2020
            sns.lineplot(ax=axes[2],x = period, y = pollutant, data=df_groupby.iloc[104:156],
                    marker = "o",label="2020")
        #axes[2].set_title("2020")

            sns.lineplot(ax=axes[3],x = period, y = pollutant, data=df_groupby.iloc[156:208],
                    marker = "o",label="2021",color="r")

        #axes[3].set_title("2021")


            sns.lineplot(ax=axes[4],x = period, y = pollutant, data=df_groupby.iloc[208:255],
                    marker = "o",label="2022",color="orange")

    #Faire un plot de la moyenne à l'année pour ensuite comparer
    plt.show()

    return

def weekday_pollutant(df,pollutant):
    """Plot each day of the week in function of the pollutant in order ot identify which a pattern between days

    """
    df_days = df.copy()
    df_days['weekday_name'] = df_days['weekday_name'].apply(lambda x: calendar.day_name[x])

    sns.barplot(data=df_days,x="weekday_name",y=f"{pollutant}")

    plt.show()

    return

def plot_shift_pollutant(df,pollutant, year):
    """Plot any pollutant with a shifting of 7 days over any year
    """
    if pollutant == "PM25":
        df["J-1"] = df["PM25"].shift(1)
        df["J-2"] = df["PM25"].shift(2)
        df["J-3"] = df["PM25"].shift(3)
        df["J-4"] = df["PM25"].shift(4)
        df["J-5"] = df["PM25"].shift(5)
        df["J-6"] = df["PM25"].shift(6)
        df["J-7"] = df["PM25"].shift(7)

    elif pollutant == "PM10":
        df["J-1"] = df["PM10"].shift(1)
        df["J-2"] = df["PM10"].shift(2)
        df["J-3"] = df["PM10"].shift(3)
        df["J-4"] = df["PM10"].shift(4)
        df["J-5"] = df["PM10"].shift(5)
        df["J-6"] = df["PM10"].shift(6)
        df["J-7"] = df["PM10"].shift(7)

    elif pollutant == "NO2":
        df["J-1"] = df["NO2"].shift(1)
        df["J-2"] = df["NO2"].shift(2)
        df["J-3"] = df["NO2"].shift(3)
        df["J-4"] = df["NO2"].shift(4)
        df["J-5"] = df["NO2"].shift(5)
        df["J-6"] = df["NO2"].shift(6)
        df["J-7"] = df["NO2"].shift(7)

    elif pollutant =="O3":
        df["J-1"] = df["O3"].shift(1)
        df["J-2"] = df["O3"].shift(2)
        df["J-3"] = df["O3"].shift(3)
        df["J-4"] = df["O3"].shift(4)
        df["J-5"] = df["O3"].shift(5)
        df["J-6"] = df["O3"].shift(6)
        df["J-7"] = df["O3"].shift(7)

    elif pollutant =="SO2":
        df["J-1"] = df["SO2"].shift(1)
        df["J-2"] = df["SO2"].shift(2)
        df["J-3"] = df["SO2"].shift(3)
        df["J-4"] = df["SO2"].shift(4)
        df["J-5"] = df["SO2"].shift(5)
        df["J-6"] = df["SO2"].shift(6)
        df["J-7"] = df["SO2"].shift(7)

    #Drop des NA des 7 premiers jours
    df = df.dropna()

    #Création de la colonne mean_shift qui est la moyenne des 7 derniers jours
    df["mean_shift"]=df[["J-1","J-2","J-3","J-4","J-5","J-6","J-7"]].mean(axis=1)
    #print(df[0:365])

    plt.figure(figsize=(20,10))

    plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

    #fig.suptitle('MEAN PM25 per Month - Per Year')

    if year == "2018":

        sns.lineplot( x = "Date_time", y = "mean_shift", data=df[0:365],
             marker = "o",label="2018",color = "red")

    elif year =="2019":
        sns.lineplot( x = "Date_time", y = "mean_shift", data=df[365:730],
             marker = "o",label="2019",color = "red")

    elif year =="2020":
        sns.lineplot( x = "Date_time", y = "mean_shift", data=df[730:1065],
             marker = "o",label="2020",color = "red")

    elif year =="2021":
        sns.lineplot( x = "Date_time", y = "mean_shift", data=df[1065:1430],
             marker = "o",label="2021",color = "red")

    elif year == "2022":
        sns.lineplot( x = "Date_time", y = "mean_shift", data=df[1430:1795],
             marker = "o",label="2022",color = "red")

    plt.show()
    return
