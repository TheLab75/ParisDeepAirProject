import streamlit as st
import requests

#from workflow.registry import predict
#from streamlit_extras.metric_cards import style_metric_cards

st.title('When should I run for the next few days')
st.header('App to get the prediction of airquality for the next 7 days')
#st.header('ATMO Features')

with st.form(key='params_for_api'):

    today = st.date_input('day')

    station = st.selectbox(
        'Select a station  ?',
        ('','Paris_south', 'Paris_east', 'Paris_north','Paris_west','Paris_center'))

    st.form_submit_button('Running plan')

params = dict(
     station=station)

api_url = 'https://deepair-5mve7fqcea-od.a.run.app/predict'
response = requests.get(api_url, params=params)

prediction = response.json()

# from streamlit_extras.let_it_rain import rain

# rain(
#     emoji="👏",
#     font_size=65,
#     falling_speed=5,
#     animation_length="infinite",
# )

#st.write(prediction)

if station != "":

    if prediction["day1"] == 1:
        reco = "You can run 🏃‍♂️"
    else:
        reco="-You shouldn't run 😿"

    if prediction["day2"] == 1:
        reco2 = "You can run 🏃‍♂️"
    else:
        reco2="-You shouldn't run 😿"

    if prediction["day3"] == 1:
        reco3= "You can run 🏃‍♂️"
    else:
        reco3="-You shouldn't run 😿"

    if prediction["day4"] == 1:
        reco4= "You can run 🏃‍♂️"
    else:
        reco4="-You shouldn't run 😿"

    if prediction["day5"] == 1:
        reco5= "You can run 🏃‍♂️"
    else:
        reco5="-You shouldn't run 😿"

    if prediction["day6"] == 1:
        reco6= "You can run 🏃‍♂️"
    else:
        reco6="-You shouldn't run 😿"

    if prediction["day7"] == 1:
        reco7= "You can run 🏃‍♂️"
    else:
        reco7="-You shouldn't run 😿"

    col1, col2, col3 = st.columns(3)
    col1.metric('',"Day 1", reco)
    col2.metric('',"Day 2", reco2)
    col3.metric('',"Day 3",reco3)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        st.write("")
    with col3:
        st.write("")

    col1, col2, col3,col4 = st.columns(4)
    col1.metric('',"Day 4", reco4)
    col2.metric('',"Day 5", reco5)
    col3.metric('',"Day 6", reco6)
    col4.metric('',"Day 7", reco7)

    st.balloons()
