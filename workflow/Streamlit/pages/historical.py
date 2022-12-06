import streamlit as st
import datetime
import requests

#Imports de base
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

st.title('What is the historical evolution of the pollution in paris ?')



with st.form(key='params_for_api'):

   station = st.selectbox(
        'Select a station  ?',
        ('16', 'South', 'West','Est','Center'))
   polluant = st.selectbox(
        'Select a polluant / ATMO ?',
        ('PM25', 'PM10', 'NO2','O3','SO2','ATMO'))

   year = st.selectbox('Select a year'
                       ,('2018', '2019', '2020','2021','2022'))
   scale = st.selectbox('Select a scale',
                        ('month','week'))


   st.write('You selected the area of paris:',station)
   st.write('You selected the polluant:',polluant)
   st.write('You selected the year:',year)
   st.write(f'You selected the {scale} scale')
   st.form_submit_button('reload')




#Data frame de Base
if station == "16":
    df = pd.read_csv("data/pollution/2_Processed/PA75016.csv")
    st.dataframe(df,200,20)
    st.write('You selected the station :', station )


#Preprocess du dataframe sans scaling
from workflow.preprocessing import preprocess_without_scaling

st.write('Now you will see the effects of processing WOW ! 🥵' )
#Voir pourquoi l'imputer ne fonctionne pas ici
df_preprocessed_without_scaling = preprocess_without_scaling(df)
st.dataframe(df_preprocessed_without_scaling,200, 20)


from workflow.data_viz import data_viz
st.write('Your dataframe will be ready for data viz ! 🥵' )
df_ready_for_data_viz = data_viz(df_preprocessed_without_scaling)
st.dataframe(df_ready_for_data_viz,200, 20)


if scale == 'month':
    #fig = plt.figure(figsize=(12,5))
        df_ready_for_data_viz = df_ready_for_data_viz.groupby(by=["year",scale],as_index=False).mean()
        df_ready_for_data_viz['month'] = df_ready_for_data_viz['month'].apply(lambda x: calendar.month_abbr[x])

        plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')

        if year == "2018":
            fig = plt.figure(figsize=(10,5))
            sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[:12],
                        marker = "o",label="2018").set_title(f"{polluant} Mean per month per Year")

        if year == "2019":
            fig = plt.figure(figsize=(10,5))
            sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[12:24],
                        marker = "o",label="2019").set_title(f"{polluant} Mean per month per Year")
        if year == "2020":
            fig = plt.figure(figsize=(10,5))
            sns.lineplot(x = scale, y =polluant, data=df_ready_for_data_viz.iloc[24:36],
                        marker = "o",label="2020").set_title(f"{polluant} Mean per month per Year")
        if year == "2021":
            fig = plt.figure(figsize=(10,5))
            sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[36:48],
                        marker = "o",label="2021").set_title(f"{polluant} Mean per month per Year")
        if year == "2022":
            fig = plt.figure(figsize=(10,5))
            sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[48:58],
                        marker = "o",label="2022").set_title(f"{polluant} Mean per month per Year")

if scale == "week":
    df_ready_for_data_viz = df_ready_for_data_viz.groupby(by=["year",scale],as_index=False).mean()

    if year == "2018":
        fig = plt.figure(figsize=(10,5))
        sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[:52],
                    marker = "o",label="2018").set_title(f"{polluant} Mean per week per Year")

    if year == "2019":
        fig = plt.figure(figsize=(10,5))
        sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[52:104],
                    marker = "o",label="2019").set_title(f"{polluant} Mean per week per Year")
    if year == "2020":
        fig = plt.figure(figsize=(10,5))
        sns.lineplot(x = scale, y =polluant, data=df_ready_for_data_viz.iloc[104:156],
                    marker = "o",label="2020").set_title(f"{polluant} Mean per week per Year")
    if year == "2021":
        fig = plt.figure(figsize=(10,5))
        sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[156:208],
                    marker = "o",label="2021").set_title(f"{polluant} Mean per week per Year")
    if year == "2022":
        fig = plt.figure(figsize=(10,5))
        sns.lineplot(x = scale, y = polluant, data=df_ready_for_data_viz.iloc[208:255],
                    marker = "o",label="2022").set_title(f"{polluant} Mean per week per Year")


st.pyplot(fig)

if polluant == "ATMO":

    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        st.write("")

    with col2:
        image = "pages/index ATMO.jpg"

        st.image(image, caption='ATMO Index')

    with col3:
        st.write("")

if polluant != 'ATMO':

    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        st.write("")

    with col2:
        image = "pages/grille polluant ATMO.jpg"

        st.image(image, caption='ATMO Index')

    with col3:
        st.write("")






# Maintenant on veut afficher un index ATMO

# from PIL import Image
# image = "pages/index ATMO.jpg"

# st.image(image, caption='ATMO Index')
