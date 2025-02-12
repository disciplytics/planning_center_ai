import streamlit as st
from streamlit_oauth import OAuth2Component
from utils.auth import pcoAuth
import requests


st.title("Planning Center Analytics")


with st.sidebar:
  oauth2 = pcoAuth()

st.write(oauth2)#.get('https://api.planningcenteronline.com/people/v2/people'))
