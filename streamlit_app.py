import streamlit as st
from streamlit_oauth import OAuth2Component
from utils.auth import pcoAuth
import pypco

st.title("Planning Center Analytics")

with st.sidebar:
  pcoAuth()

if 'token' not in st.session_state:
  st.write('Please log into Planning Center to get started.')
else:
  # Once you've gotten your access token, you can initialize a pypco object like this:
  pco = pypco.PCO(token=st.session_state.token['access_token'])
  
  # Now, you're ready to go.
  # The iterate() function provides an easy way to retrieve lists of objects
  # from an API endpoint, and automatically handles pagination
  people = pco.iterate('/people/v2/people?include=addresses,emails,field_data,households,inactive_reason,marital_status,organization,phone_numbers,primary_campus')
  person = next(people)
  
  st.write(people)
  
