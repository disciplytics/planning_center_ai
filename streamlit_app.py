import streamlit as st
from streamlit_oauth import OAuth2Component
from utils.auth import pcoAuth
import requests
from requests_oauthlib import OAuth1


# Set environment variables
AUTHORIZE_URL = st.secrets["AUTHORIZE_URL"]
TOKEN_URL = st.secrets["TOKEN_URL"]
REFRESH_TOKEN_URL = st.secrets["TOKEN_URL"]
REVOKE_TOKEN_URL = st.secrets["REVOKE_TOKEN_URL"]
CLIENT_ID = st.secrets["PC_CLIENT_ID"]
CLIENT_SECRET = st.secrets["PC_CLIENT_SECRET"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]
SCOPE = st.secrets["SCOPE"]

st.title("Planning Center Analytics")

import pypco



with st.sidebar:
  pcoAuth()

pco = pypco.PCO(st.session_state.token)

st.write(pco.get('/people/v2/people'))#.get('https://api.planningcenteronline.com/people/v2/people'))
