import streamlit as st
from utils.auth import pcoAuth
from reports.attendance import attendance_trend
import pandas as pd
import numpy as np
import altair as alt
# PAGE CONGIG
st.set_page_config(
        page_title="Household Health Monitor", 
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
        st.write('Household Health Report')

        @st.cache_data
        def household_health_report():
                return 'hello'


