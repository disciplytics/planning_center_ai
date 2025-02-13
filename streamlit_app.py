import streamlit as st
from streamlit_oauth import OAuth2Component
from utils.auth import pcoAuth
import pypco

st.logo(width=100, "https://jimdo-storage.freetls.fastly.net/image/446612637/7c401e7a-6b6d-4ec8-84a5-4ab2cae82c9e.png?quality=80,90&auto=webp&disable=upscale&width=480&height=270&trim=0,0,0,0")
st.title("Planning Center Analytics")

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
  
