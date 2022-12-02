#Imports de base
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar


def data_viz(df):
    """Cette fonction nécessite comme un argument un dataframe préprocessed mais non sans le scaling

    """

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
    df_all_week = df.groupby(by=["year","week"],as_index=False).mean()

    #Création d'un dataframe groupé par année et par mois
    df_all_month = df.groupby(by=["year","month"],as_index=False).mean()

    #Passage des mois allant de 1 à 12 en Janvier à Décembre
    df_all_month['month'] = df_all_month['month'].apply(lambda x: calendar.month_abbr[x])

    #Passage des jours de la semaine allant de 0 à 6 en Lundi jusque Dimanche
    df_days = df.copy()
    df_days['weekday_name'] = df_days['weekday_name'].apply(lambda x: calendar.day_name[x])

    plot_1 = plot_PM25_month(df_all_month)
    plot_2 = plot_PM25_Month_2(df_all_month)

    plot_3 = weekday_barplot_ATMO(df_days)
    plot_4 = weekday_barplot_PM25(df_days)


    return plot_1,plot_2,plot_3,plot_4


def plot_PM25_month(df_all_month):

    plt.figure(figsize=(12,5))

    #plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')


    ax1 = sns.lineplot(x = "month", y = "PM25", data=df_all_month.iloc[:12],
                marker = "o",label="2018")

    sns.lineplot(x = "month", y = "PM25", data=df_all_month.iloc[12:24],
                marker = "o",label="2019")

    sns.lineplot(x = "month", y ="PM25", data=df_all_month.iloc[24:36],
                marker = "o",label="2020")

    sns.lineplot(x = "month", y = "PM25", data=df_all_month.iloc[36:48],
                marker = "o",label="2021")

    sns.lineplot(x = "month", y = "PM25", data=df_all_month.iloc[48:59],
                marker = "o",label="2022").set_title("PM 25 Mean per month per Year")



    ax1.text("Apr",58,"1er Confinement",
        fontsize = 7,          # Size
        fontstyle = "italic",  # Style
        color = "white",          # Color
        ha = "center", # Horizontal alignment
        va = "center") # Vertical alignment


    ax1.text("Nov",58,"2ème Confinement",
        fontsize = 7,          # Size
        fontstyle = "italic",  # Style
        color = "white",          # Color
        ha = "center", # Horizontal alignment
        va = "center") # Vertical alignment

    ax1.text("May",58,"3ème Confinement",
        fontsize = 7,          # Size
        fontstyle = "italic",  # Style
        color = "white",          # Color
        ha = "center", # Horizontal alignment
        va = "top") # Vertical alignment


    plt.show()

    return


def plot_PM25_Month_2(df_all_month):

    fig, axes = plt.subplots(5, 1, figsize=(18, 18), sharey=True)


    fig.suptitle('MEAN PM25 per Month - Per Year')


    # 2018
    sns.lineplot(ax=axes[0], x = "month", y = "PM25", data=df_all_month.iloc[:12],
                marker = "o",label="2018",color = "green")
    #axes[0].set_title("2018")

    #sns.lineplot(ax=axes[0], x = "month", y = "PM25", data=df_all_month.iloc[:12],
                # marker = "o",label="2018",color = "green")


    # 2019
    sns.lineplot(ax=axes[1],x = "month", y = "PM25", data=df_all_month.iloc[12:24],
                marker = "o",label="2019",color="b")
    #axes[1].set_title("2019")

    sns.lineplot(ax=axes[2],x = "month", y ="PM25", data=df_all_month.iloc[24:36],
                marker = "o",label="2020")
    #axes[2].set_title("2020")

    sns.lineplot(ax=axes[3],x = "month", y = "PM25", data=df_all_month.iloc[36:48],
                marker = "o",label="2021",color="r")

    #axes[3].set_title("2021")


    sns.lineplot(ax=axes[4],x = "month", y = "PM25", data=df_all_month.iloc[48:59],
                marker = "o",label="2022",color="orange")


    #axes[4].set_title("2022")


    #Faire un plot de la moyenne à l'année pour ensuite comparer
    plt.show()

    return


def weekday_barplot_ATMO(df_days):

    sns.barplot(data=df_days,x="weekday_name",y="ATMO")


    plt.show()
    return

def weekday_barplot_PM25(df_days):

    sns.barplot(data=df_days,x="weekday_name",y="PM25")

    plt.show()
    return
