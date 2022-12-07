import streamlit as st
import requests

from workflow.registry import predict



st.title('When should I run for the next few days')
st.markdown('app to get the prediction of airquality')
st.header('ATMO Features')

with st.form(key='params_for_api'):

    today = st.date_input('day')


    station = st.selectbox(
        'Select a station  ?',
        ('Paris_est', 'Paris_south', 'Paris_north','Paris_west','Paris_center',"All"))

    st.form_submit_button('Predict')



params = dict(
     station=station)



api_url = 'http://localhost:8000/predict'
response = requests.get(api_url, params=params)

prediction = response.json()


st.write(prediction)
