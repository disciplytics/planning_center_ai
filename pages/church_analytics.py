import streamlit as st
from utils.auth import pcoAuth
from reports.attendance import attendance_trend
import pandas as pd
import numpy as np
import altair as alt
from st_paywall import add_auth
import pypco 
from utils.pco_elt import pco_elt   

# PAGE CONGIG
st.set_page_config(
        page_title="Church Analytics", 
        layout="wide",
        page_icon = 'https://jimdo-storage.freetls.fastly.net/image/446612637/7c401e7a-6b6d-4ec8-84a5-4ab2cae82c9e.png?quality=80,90&auto=webp&disable=upscale&width=1024&height=576&trim=0,0,0,0',
)

# LOGO
st.image("https://media.licdn.com/dms/image/v2/D4E16AQGCrog5mV8nBQ/profile-displaybackgroundimage-shrink_350_1400/B4EZUAA8ZzHgAY-/0/1739462002589?e=1744848000&v=beta&t=miQyzZN82YjcYs9B_Mc-UVhaKt01dqVnPE56CnaVPbw",
        width = 250)


# PCO AUTH 
if 'token' not in st.session_state:
    st.switch_page("pages/pco_integration.py")   
else:
    pco = pypco.PCO(token=st.session_state.token['access_token'])
    st.write('Household Health Report')

    st.write(pco.get('/people/v2/me')['meta']['parent']['id'])

    st.dataframe(pco_elt(pco))
