import streamlit as st
import requests

from workflow.registry import predict
from streamlit_extras.metric_cards import style_metric_cards



st.title('When should I run for the next few days')
st.markdown('app to get the prediction of airquality')
st.header('ATMO Features')

with st.form(key='params_for_api'):

    today = st.date_input('day')


    station = st.selectbox(
        'Select a station  ?',
        ('Paris_east', 'Paris_south', 'Paris_north','Paris_west','Paris_center',"All"))

    st.form_submit_button('Predict')



params = dict(
     station=station)



api_url = 'http://localhost:8000/predict'
response = requests.get(api_url, params=params)

prediction = response.json()


#st.write(prediction)



# col1, col2, col3,col4 = st.columns(3)
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


#if prediction == 0:

if station != "All":

    if prediction["day1"] == 1:
        reco = "You can run"
    else:
        reco="-You can't run"

    if prediction["day2"] == 1:
        reco2 = "You can run"
    else:
        reco2="-You can't run"


    if prediction["day3"] == 1:
        reco3= "You can run"
    else:
        reco3="-You can't run"


    if prediction["day4"] == 1:
        reco4= "You can run"
    else:
        reco4="-You can't run"


    if prediction["day5"] == 1:
        reco5= "You can run"
    else:
        reco5="-You can't run"


    if prediction["day6"] == 1:
        reco6= "You can run"
    else:
        reco6="-You can't run"


    if prediction["day7"] == 1:
        reco7= "You can run"
    else:
        reco7="-You can't run"



    col1, col2, col3 = st.columns(3)
    col1.metric("Air Quality", "Day 1", reco)
    col2.metric("Air Quality", "Day 2", reco2)
    col3.metric("Air Quality", "Day 3",reco3)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("")
    with col2:
        st.write("")
    with col3:
        st.write("")


    col1, col2, col3,col4 = st.columns(4)
    col1.metric("Air Quality", "Day 4", reco4)
    col2.metric("Air Quality", "Day 5", reco5)
    col3.metric("Air Quality", "Day 6", reco6)
    col4.metric("Air Quality", "Day 7", reco7)
