import streamlit as st
from streamlit_oauth import OAuth2Component
from utils.auth import pcoAuth
import requests


st.title("Planning Center Analytics")


with st.sidebar:
  pcoAuth()

st.write(st.session_state.token)#.get('https://api.planningcenteronline.com/people/v2/people'))
