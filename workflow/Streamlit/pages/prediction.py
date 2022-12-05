import streamlit as st

from datetime import datetime
from workflow.main_local import Model
from workflow.main_local import load_model

#@st.cache
#model_load =load_model()

st.title('Where I should run for the next few days')
st.markdown('app to get the prediction of airquality')
st.header('ATMO Features')

with st.form(key='params_for_api'):

    today = st.date_input('day')
    "put today date ",
    st.write('today is:', today)



    st.form_submit_button('reload')










#predict(model, X_test)
