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
    print(os.path.abspath(f"workflow/Streamlit/assets/pollution/5_Clusters/{element}.csv"))
    df=pd.read_csv(os.path.abspath(f"workflow/Streamlit/assets/pollution/5_Clusters/{element}.csv"))

if station == "Paris South":
    element = "cluster4_Sud"
    print(os.path.abspath(f"workflow/Streamlit/assets/pollution/5_Clusters/{element}.csv"))
    df=pd.read_csv(os.path.abspath(f"workflow/Streamlit/assets/pollution/5_Clusters/{element}.csv"))

if station == "Paris West":
    element = "cluster1_Ouest"
    print(os.path.abspath(f"workflow/Streamlit/assets/pollution/5_Clusters/{element}.csv"))
    df=pd.read_csv(os.path.abspath(f"workflow/Streamlit/assets/pollution/5_Clusters/{element}.csv"))

if station == "Paris East":
    element = "cluster3_Est"
    print(os.path.abspath(f"workflow/Streamlit/assets/pollution/5_Clusters/{element}.csv"))
    df=pd.read_csv(os.path.abspath(f"workflow/Streamlit/assets/pollution/5_Clusters/{element}.csv"))

if station == "Paris Center":
    element = "cluster5_Centre"
    print(os.path.abspath(f"workflow/Streamlit/assets/pollution/5_Clusters/{element}.csv"))
    df=pd.read_csv(os.path.abspath(f"workflow/Streamlit/assets/pollution/5_Clusters/{element}.csv"))

#Preprocess du dataframe sans scaling
from workflow.preprocessing import preprocess_without_scaling

# st.write('Now you will see the effects of processing WOW ! 🥵' )
# #Voir pourquoi l'imputer ne fonctionne pas ici
df_preprocessed_without_scaling = preprocess_without_scaling(df)
# st.dataframe(df_preprocessed_without_scaling,200, 20)


from workflow.data_viz import data_viz
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
