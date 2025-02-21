import streamlit as st
from utils.auth import pcoAuth
from reports.attendance import attendance_trend
import pandas as pd

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
        with st.container():
                st.write("Headcount Metrics")
                st.session_state.headcounts_df['Headcount Type'] = st.session_state.headcounts_df['attributes.name_at']
                st.session_state.headcounts_df['attributes.total'] = st.session_state.headcounts_df['attributes.total'].astype('int32')
                st.session_state.headcounts_df['attributes.starts_at_at'] = st.session_state.headcounts_df['attributes.starts_at_at'].astype('datetime64[ns]')
                st.bar_chart(data=st.session_state.headcounts_df, x='attributes.starts_at_at', y='attributes.total', x_label='Date', y_label='Headcounts', color='Headcount Type',)# horizontal=False, stack=None, width=None, height=None, use_container_width=True)
        
        
                st.write(st.session_state.headcounts_df)

 
        
        #st.dataframe(st.session_state.households_df)
        #st.write(st.session_state.donations_df)
