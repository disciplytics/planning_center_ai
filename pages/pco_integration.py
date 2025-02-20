import streamlit as st
from streamlit_oauth import OAuth2Component
from utils.auth import pcoAuth
import pypco
import pandas as pd
import asyncio
from utils.load_data import load_data


# PAGE CONGIG
st.set_page_config(
        page_title="Planning Center Integration", 
        layout="wide",
        page_icon = 'https://jimdo-storage.freetls.fastly.net/image/446612637/7c401e7a-6b6d-4ec8-84a5-4ab2cae82c9e.png?quality=80,90&auto=webp&disable=upscale&width=1024&height=576&trim=0,0,0,0',
)

# LOGO
st.image("https://media.licdn.com/dms/image/v2/D4E16AQGCrog5mV8nBQ/profile-displaybackgroundimage-shrink_350_1400/B4EZUAA8ZzHgAY-/0/1739462002589?e=1744848000&v=beta&t=miQyzZN82YjcYs9B_Mc-UVhaKt01dqVnPE56CnaVPbw",
        width = 250)

# PAGE TITLE
st.title("Planning Center Integration")


# PCO AUTH 
if 'token' not in st.session_state:
        st.write('Please authorize our app to access your Planning Center data.')
        pcoAuth()
else:
        st.write('You are logged in!')
        # Once you've gotten your access token, you can initialize a pypco object like this:
        pco = pypco.PCO(token=st.session_state.token['access_token'])
                
        # load data from pco
        st.session_state.people_df, st.session_state.household_df = load_data(pco)

        if st.button("Logout"):
                del st.session_state["token"]
                del st.session_state["people_df"]
                del st.session_state["household_df"]

