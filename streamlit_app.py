import streamlit as st
from streamlit_oauth import OAuth2Component
from utils.auth import pcoAuth
import pypco
import pandas as pd
import asyncio
from utils.load_data import load_data

st.set_page_config(page_title="Planning Center Analytics App", layout="wide")

st.image("https://media.licdn.com/dms/image/v2/D4E16AQGCrog5mV8nBQ/profile-displaybackgroundimage-shrink_350_1400/B4EZUAA8ZzHgAY-/0/1739462002589?e=1744848000&v=beta&t=miQyzZN82YjcYs9B_Mc-UVhaKt01dqVnPE56CnaVPbw",
        width = 250)
st.title("Planning Center Analytics")



#with st.sidebar:
#  pcoAuth()

if 'token' not in st.session_state:
  st.write('Please authorize our app to access your Planning Center data.')
  pcoAuth()
else:
  # Once you've gotten your access token, you can initialize a pypco object like this:
  pco = pypco.PCO(token=st.session_state.token['access_token'])

  # load data from pco
  people_df, household_df = load_data(pco)
  # do reporting
        
  st.dataframe(pd.json_normalize(household_df))
  st.dataframe(pd.json_normalize(people_df))

  st.session_state.people_df_logged = people_df

  st.dataframe(pd.json_normalize(st.session_state.people_df_logged))

  #st.write(st.session_state)
