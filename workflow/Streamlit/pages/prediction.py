import streamlit as st

from datetime import datetime
#from workflow.main_local import Model
from workflow.main_local import load_model
#from workflow.api import

#@st.cache
#model_load =load_model()

st.title('When should I run for the next few days')
st.markdown('app to get the prediction of airquality')
st.header('ATMO Features')

with st.form(key='params_for_api'):

    today = st.date_input('day')


    station = st.selectbox(
        'Select a station  ?',
        ('Paris_est', 'Paris_south', 'Paris_north','Paris_west','Paris_center'))

    st.form_submit_button('Predict')

# params = dict(
#     pickup_datetime=pickup_datetime,
#     pickup_longitude=pickup_longitude,
#     pickup_latitude=pickup_latitude,
#     dropoff_longitude=dropoff_longitude,
#     dropoff_latitude=dropoff_latitude,
#     passenger_count=passenger_count)

# wagon_cab_api_url = 'https://taxifare.lewagon.ai/predict'
# response = requests.get(wagon_cab_api_url, params=params)

# prediction = response.json()

# pred = prediction['fare']

# st.header(f'Fare amount: ${round(pred, 2)}')








#predict(model, X_test)
