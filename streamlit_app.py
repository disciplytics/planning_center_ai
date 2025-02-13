import streamlit as st
from streamlit_oauth import OAuth2Component
from utils.auth import pcoAuth
import pypco


logo, title = st.columns([.3,.7])
logo.image("https://raw.githubusercontent.com/disciplytics/planning_center_ai/main/utils/1200px-dl_dark_logo.svg.png",)
title.title("Planning Center Analytics")


#"https://raw.githubusercontent.com/djswoosh/Music-Recommendation-Engine-using-FMA-Dataset/main/1200px-The_Echo_Nest_logo.svg.png"


#with st.sidebar:
#  pcoAuth()

if 'token' not in st.session_state:
  st.write('Please authorize our app access to your Planning Center data.')
  pcoAuth()
else:
  # Once you've gotten your access token, you can initialize a pypco object like this:
  pco = pypco.PCO(token=st.session_state.token['access_token'])
  
  # Now, you're ready to go.
  # The iterate() function provides an easy way to retrieve lists of objects
  # from an API endpoint, and automatically handles pagination
  people = pco.iterate('/people/v2/people?include=addresses,emails,field_data,households,inactive_reason,marital_status,organization,phone_numbers,primary_campus')
  person = next(people)
  
  st.write(people)
  
