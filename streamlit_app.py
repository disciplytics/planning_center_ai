import streamlit as st
from streamlit_oauth import OAuth2Component
from utils.auth import pcoAuth
st.title("hello")


pcoAuth()
