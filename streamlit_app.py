import streamlit as st
from streamlit_oauth import OAuth2Component
from utils.auth import pcoAuth
import pypco

st.title("Planning Center Analytics")

with st.sidebar:
  pcoAuth()

# Once you've gotten your access token, you can initialize a pypco object like this:
pco = pypco.PCO(token=st.session_state.token['access_token'])

# Now, you're ready to go.
# The iterate() function provides an easy way to retrieve lists of objects
# from an API endpoint, and automatically handles pagination
people = pco.iterate('/people/v2/people?include=households')
person = next(people)

st.write(people)
