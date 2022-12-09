import streamlit as st
import datetime
import requests



# Title of the page
#st.title('Welcome to Paris-DeepAir-Project')

# Header & sub_header
#st.header('today we have the opportunity to present you a revolutionary tool to enjoy Paris safely')
#st.subheader('-in order to go for a walk')
#st.subheader('- in order to run')
#st.text('all while allowing you to limit your risk of exposure to harmful pollutant for your health')


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Paris-DeepAir-Project! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Paris_Deepair is an open-source application framework built specifically for Parisian citizens to find out the air quality in Paris up to 7 days in advance with an overall recall rate of 80%.


    ### Want to learn more?
    - Check out [Atmo-France](https://www.atmo-france.org/article/lindice-atmo)
    - Other provider [The air quality observatory in Île-de-France](https://www.airparif.asso.fr/accueil-airparif)
    - Research paper on the subject [Air-pollution prediction in smart city, deep learning approach](https://journalofbigdata.springeropen.com/articles/10.1186/s40537-021-00548-1)
"""
)

col1, col2, col3 = st.columns([1,6,1])

with col1:
    st.write("")

with col2:
    st.image("https://hospitality-on.com/sites/default/files/2017-09/Paris.jpg",width=700)
    #st.image("workflow/Streamlit/Capture d’écran 2022-12-01 à 01.11.40-min.jpg")

with col3:
    st.write("")


# col1, col2, col3 = st.columns([1,6,1])

# with col1:
#     st.write("")

# with col2:

#         #from PIL import Image
#         #image = Image.open("pages/index ATMO.jpg")
#     st.image("https://user-images.githubusercontent.com/108631539/204822631-d93a64e9-7ee2-496f-8e9a-623b6d60ef37.jpeg",caption='ATMO Index')


# with col3:
#     st.write("")



#st.image(
            #'https://hospitality-on.com/sites/default/files/2017-09/Paris.jpg',
            #width=600, # Manually Adjust the width of the image as per requirement
        #)
#from PIL import Image
#img = Image.open('https://hospitality-on.com/sites/default/files/2017-09/Paris.jpg')
#st.image(img,width=300,caption='Paris-DeepAir')
