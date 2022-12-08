import os
import streamlit as st
import datetime
import requests
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Imports de base
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

st.title('What is the historical evolution of the pollution in paris ?')

#from streamlit_extras.app_logo import add_logo

#add_logo("http://placekitten.com/120/120")
#st.write("👈 Check out the cat in the nav-bar!")

#uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
#for uploaded_file in uploaded_files:
#    bytes_data = uploaded_file.read()
#    st.write("filename:", uploaded_file.name)
#    st.write(bytes_data)

with st.form(key='params_for_api'):

    station = st.selectbox(
        'Select a station  ?',
        ('Paris North', 'Paris South', 'Paris West','Paris East','Paris Center'))

    df = pd.read_csv

    polluant = st.selectbox(
        'Select a polluant / ATMO ?',
        ('PM25', 'PM10', 'NO2','O3','SO2','ATMO'))

    year = st.selectbox('Select a year'
                       ,('2018', '2019', '2020','2021','2022',"2018-2022"))

    scale = st.selectbox('Select a scale',
                        ('month','week'))


#    st.write('You selected the area of paris:',station)
#    st.write('You selected the polluant:',polluant)
#    st.write('You selected the year:',year)
#    st.write(f'You selected the {scale} scale')
    st.form_submit_button('reload')

#Data frame de Base
# if station == "Paris 16":
#     element = "PA75016"
#     df = pd.read_csv("data/data/pollution/2_Processed/"f"{element}"".csv")
    # st.dataframe(df,200,20)
    # st.write('You selected the station :', station )

if station == "Paris North":
    element = "cluster2_Nord"
    df=pd.read_csv(os.path.abspath(f"workflow/Streamlit/assets/pollution/5_Clusters/{element}.csv"))

if station == "Paris South":
    element = "cluster4_Sud"
    df=pd.read_csv(os.path.abspath(f"workflow/Streamlit/assets/pollution/5_Clusters/{element}.csv"))

if station == "Paris West":
    element = "cluster1_Ouest"
    df=pd.read_csv(os.path.abspath(f"workflow/Streamlit/assets/pollution/5_Clusters/{element}.csv"))

if station == "Paris East":
    element = "cluster3_Est"
    df=pd.read_csv(os.path.abspath(f"workflow/Streamlit/assets/pollution/5_Clusters/{element}.csv"))

if station == "Paris Center":
    element = "cluster5_Centre"
    df=pd.read_csv(os.path.abspath(f"workflow/Streamlit/assets/pollution/5_Clusters/{element}.csv"))

#Preprocess du dataframe sans scaling
def preprocess_without_scaling(df):
    """
    Fonction utilisée pour preprocesser une station sans la scaler afin de pouvoir faire de la data viz sur cette station
    """

    df = df[:-25]
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

# st.write('Now you will see the effects of processing WOW ! 🥵' )
# #Voir pourquoi l'imputer ne fonctionne pas ici
df_preprocessed_without_scaling = preprocess_without_scaling(df)
# st.dataframe(df_preprocessed_without_scaling,200, 20)


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

# st.write('Your dataframe will be ready for data viz ! 🥵' )
df_ready_for_data_viz = data_viz(df_preprocessed_without_scaling)
# st.dataframe(df_ready_for_data_viz,200, 20)


if scale == 'month':
    #fig = plt.figure(figsize=(12,5))
        df_ready_for_data_viz = df_ready_for_data_viz.groupby(by=["year",scale],as_index=False).mean()
        df_ready_for_data_viz['month'] = df_ready_for_data_viz['month'].apply(lambda x: calendar.month_abbr[x])

        df_mean_all_year = df_ready_for_data_viz.groupby(by=[scale],as_index=False).mean()



        plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle')

        if year == "2018":
            fig = plt.figure(figsize=(10,5))
            sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[:12],
                        marker = "o",label="2018").set_title(f"{polluant} Mean per month per Year")

            sns.lineplot(x = scale, y = polluant, data=df_mean_all_year,
                        marker = "o",label="Mean per month of all years",c="orange")


        if year == "2019":
            fig = plt.figure(figsize=(10,5))
            sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[12:24],
                        marker = "o",label="2019").set_title(f"{polluant} Mean per month per Year")

            sns.lineplot(x = scale, y = polluant, data=df_mean_all_year,
                        marker = "o",label="Mean per month of all years",c="orange")


        if year == "2020":
            fig = plt.figure(figsize=(10,5))
            sns.lineplot(x = scale, y =polluant, data=df_ready_for_data_viz.iloc[24:36],
                        marker = "o",label="2020").set_title(f"{polluant} Mean per month per Year")
            sns.lineplot(x = scale, y = polluant, data=df_mean_all_year,
                        marker = "o",label="Mean per month of all years",c="orange")

        if year == "2021":
            fig = plt.figure(figsize=(10,5))
            sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[36:48],
                        marker = "o",label="2021").set_title(f"{polluant} Mean per month per Year")
            sns.lineplot(x = scale, y = polluant, data=df_mean_all_year,
                        marker = "o",label="Mean per month of all years",c="orange")

        if year == "2022":
            fig = plt.figure(figsize=(10,5))
            sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[48:58],
                        marker = "o",label="2022").set_title(f"{polluant} Mean per month per Year")

            sns.lineplot(x = scale, y = polluant, data=df_mean_all_year,
                        marker = "o",label="Mean per month of all years",c="orange")


        if year =="2018-2022":
            fig = plt.figure(figsize=(10,5))
            sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz,
                        marker = "o",label="2018-2022").set_title(f"{polluant} Mean per month between 2018-2022")

            sns.lineplot(x = scale, y = polluant, data=df_mean_all_year,
                        marker = "o",label="Mean per month of all years",c="orange")


if scale == "week":
    df_ready_for_data_viz = df_ready_for_data_viz.groupby(by=["year",scale],as_index=False).mean()

    df_mean_all_week = df_ready_for_data_viz.groupby(by=[scale],as_index=False).mean()


    if year == "2018":
        fig = plt.figure(figsize=(10,5))
        sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[:52],
                    marker = "o",label="2018").set_title(f"{polluant} Mean per week per Year")

        sns.lineplot(x = scale, y = polluant, data=df_mean_all_week,
                        marker = "o",label="Mean per month of all years",c="orange")

    if year == "2019":
        fig = plt.figure(figsize=(10,5))
        sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[52:104],
                    marker = "o",label="2019").set_title(f"{polluant} Mean per week per Year")
        sns.lineplot(x = scale, y = polluant, data=df_mean_all_week,
                        marker = "o",label="Mean per month of all years",c="orange")

    if year == "2020":
        fig = plt.figure(figsize=(10,5))
        sns.lineplot(x = scale, y =polluant, data=df_ready_for_data_viz.iloc[104:156],
                    marker = "o",label="2020").set_title(f"{polluant} Mean per week per Year")
        sns.lineplot(x = scale, y = polluant, data=df_mean_all_week,
                        marker = "o",label="Mean per month of all years",c="orange")

    if year == "2021":
        fig = plt.figure(figsize=(10,5))
        sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[156:208],
                    marker = "o",label="2021").set_title(f"{polluant} Mean per week per Year")
        sns.lineplot(x = scale, y = polluant, data=df_mean_all_week,
                        marker = "o",label="Mean per month of all years",c="orange")

    if year == "2022":
        fig = plt.figure(figsize=(10,5))
        sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[208:255],
                    marker = "o",label="2022").set_title(f"{polluant} Mean per week per Year")
        sns.lineplot(x = scale, y = polluant, data=df_mean_all_week,
                        marker = "o",label="Mean per month of all years",c="orange")

    if year == "2018-2022":
        fig = plt.figure(figsize=(10,5))
        sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz,
                    marker = "o",label="2018-2022").set_title(f"{polluant} Mean per week between 2018-2022")
        sns.lineplot(x = scale, y = polluant, data=df_mean_all_week,
                        marker = "o",label="Mean per month of all years",c="orange")



st.pyplot(fig)

if polluant == "ATMO":

    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        st.write("")

    with col2:

        #from PIL import Image
        #image = Image.open("pages/index ATMO.jpg")
        image = 'workflow/Streamlit/index ATMO.jpg'
        st.image(image, caption='ATMO Index')

    with col3:
        st.write("")

if polluant != 'ATMO':

    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        st.write("")

    with col2:
        # from PIL import Image
        # image = Image.open("pages/grille polluant ATMO.jpg")
        #image = "pages/grille polluant ATMO.jpg"
        st.image("https://user-images.githubusercontent.com/108631539/204822631-d93a64e9-7ee2-496f-8e9a-623b6d60ef37.jpeg",caption='ATMO Index')
        #st.image(image, caption='ATMO Index')


    with col3:
        st.write("")

# from streamlit_extras.stodo import to_do

# to_do(
#     [(st.write, "❤️ Index ATMO")],
#     "index ATMO ",)


# from streamlit_extras.metric_cards import style_metric_cards

# col1, col2, col3,col4 = st.columns(4)
# col1.metric(label="ATMO J+1 ", value=" ✅ Great",delta=-1)
# col2.metric(label="ATMO J+2", value=5000, delta=-1000)
# col3.metric(label="ATMO J+3", value=5000, delta=0)
# col4.metric(label="ATMO J+4",value="🚫 Bad ",delta =-1 )

# style_metric_cards()

# col5,col6,col7=  st.columns(3)
# col5.metric(label="ATMO J+5",value="🚫 Bad ",delta =-1 )
# col6.metric(label="ATMO J+6",value="🚫 Bad ",delta =-1 )
# col7.metric(label="ATMO J+7",value="🚫 Bad ",delta =-1 )
# style_metric_cards()




if scale == "week":

    if year == "2018":

        #sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[:52],
                    #marker = "o",label="2018").set_title(f"{polluant} Mean per week per Year")

        #fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig = px.bar(df_ready_for_data_viz.iloc[:52],x =scale, y = polluant,template= 'seaborn',
                     title=f"{polluant} Mean per week per Year",
                     text_auto='.3s',
                     color=polluant)


        fig.update_traces(marker_color = 'blue')

        #fig.add_trace(px.line(df_mean_all_week,x=scale,y=polluant))

        #fig = px.line(df_mean_all_week,x=scale,y=polluant)


        # sns.lineplot(x = scale, y = polluant, data=df_mean_all_week,
        #                 marker = "o",label="Mean per month of all years",c="orange")


    if year == "2019":

        fig = px.bar(df_ready_for_data_viz.iloc[52:104],x =scale, y = polluant,template= 'seaborn',
                     title=f"{polluant} Mean per week per Year",
                     text_auto='.3s',
                     color=polluant)

    if year == "2020":
        fig = px.bar(df_ready_for_data_viz.iloc[104:156],x =scale, y = polluant,template= 'seaborn',
                     title=f"{polluant} Mean per week per Year",
                     text_auto='.3s',
                     color=polluant)
    if year == "2021":
        fig = px.bar(df_ready_for_data_viz.iloc[156:208],x =scale, y = polluant,template= 'seaborn',
                     title=f"{polluant} Mean per week per Year",
                     text_auto='.3s',
                     color=polluant)

    if year == "2022":
        fig = px.bar(df_ready_for_data_viz.iloc[208:255],x =scale, y = polluant,template= 'seaborn',
                     title=f"{polluant} Mean per week per Year",
                     text_auto='.3s',
                     color=polluant)

    if year == "2018-2022":
        fig = px.bar(df_ready_for_data_viz,x =scale, y = polluant,template= 'seaborn',
                     title=f"{polluant} Mean per week between 2018-2022",
                     text_auto='.3s',
                     color=polluant)

    st.plotly_chart(fig, use_container_width=True)

if scale == "month":


    if year == "2018":

        #sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[:52],
                    #marker = "o",label="2018").set_title(f"{polluant} Mean per week per Year")



        fig = px.bar(df_ready_for_data_viz.iloc[:12],x =scale, y = polluant,template= 'seaborn',
                     title=f"{polluant} Mean per month per Year",
                     text_auto='.3s',
                     color=polluant)

        #fig.update_traces(marker_color = 'green')
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

        #Slider
#         fig.update_layout(xaxis=dict(
#         rangeselector=dict(
#             buttons=list([
#                 dict(count=1,
#                      label="1m",
#                      step="month",
#                      stepmode="backward"),
#                 dict(count=6,
#                      label="6m",
#                      step="month",
#                      stepmode="backward"),
#                 dict(count=1,
#                      label="YTD",
#                      step="year",
#                      stepmode="todate"),
#                 dict(count=1,
#                      label="1y",
#                      step="year",
#                      stepmode="backward"),
#                 dict(step="all")
#             ])
#         ),
#         rangeslider=dict(
#             visible=True
#         ),
#         type="date"
#     )
# )


        #fig.add_trace(px.line(df_mean_all_week,x=scale,y=polluant))

        #fig = px.line(df_mean_all_week,x=scale,y=polluant)



        #fig.add_bar(df_ready_for_data_viz.iloc[:12],x =scale, y = polluant,template= 'seaborn', title=f"{polluant} Mean per month per Year")
        #fig.update_traces(marker_color = 'green')

        # sns.lineplot(x = scale, y = polluant, data=df_mean_all_week,
        #                 marker = "o",label="Mean per month of all years",c="orange")


    if year == "2019":
        fig = px.bar(df_ready_for_data_viz.iloc[12:24],x =scale, y = polluant,template= 'seaborn',
                     title=f"{polluant} Mean per month per Year",
                     text_auto='.3s',
                     color=polluant)

        #fig.update_traces(marker_color = 'green')
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    if year == "2020":
        fig = px.bar(df_ready_for_data_viz.iloc[24:36],x =scale, y = polluant,template= 'seaborn',
                     title=f"{polluant} Mean per month per Year",
                     text_auto='.3s',
                     color=polluant)

        #fig.update_traces(marker_color = 'green')
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    if year == "2021":
        fig = px.bar(df_ready_for_data_viz.iloc[36:48],x =scale, y = polluant,template= 'seaborn',
                     title=f"{polluant} Mean per month per Year",
                     text_auto='.3s',
                     color=polluant)

        #fig.update_traces(marker_color = 'green')
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    if year == "2022":
        fig = px.bar(df_ready_for_data_viz.iloc[48:60],x =scale, y = polluant,template= 'seaborn',
                     title=f"{polluant} Mean per month per Year",
                     text_auto='.3s',
                     color=polluant)

        #fig.update_traces(marker_color = 'green')
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    if year == "2018-2022":
        fig = px.bar(df_ready_for_data_viz,x =scale, y = polluant,template= 'seaborn',
                     title=f"{polluant} Mean per month between 2018-2022",
                     text_auto='.3s',
                     color=polluant)
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)





    st.plotly_chart(fig, use_container_width=True)
