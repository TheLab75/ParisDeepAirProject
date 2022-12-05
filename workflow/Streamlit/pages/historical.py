import streamlit as st
import datetime
import requests

st.title('Historical evolution of the dominant pollutants')




with st.form(key='params_for_api'):

    station = st.selectbox(
        'Select a area of paris ?',
        ('North', 'South', 'West','Est','Center'))

    polluant = st.selectbox(
        'Select a polluant ?',
        ('PM2.5', 'PM10', 'NO2','O3','SO2'))

    year = st.selectbox('Select a year',('2018', '2019', '2020','2021','2022'))

    st.write('You selected the area of paris:',station)
    st.write('You selected the polluant:',polluant)
    st.write('You selected the year:',year)


    st.form_submit_button('reload')
