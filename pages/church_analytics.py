import streamlit as st
from utils.auth import pcoAuth
from reports.attendance import attendance_trend
import pandas as pd
import numpy as np

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
        @st.cache_data
        def headcounts_trend(data):
                data['Headcount Type'] = data['attributes.name_at']
                data['Headcounts'] = pd.to_numeric(data['attributes.total'])
                data['Date'] = pd.to_datetime(data['attributes.starts_at'], utc=True).dt.date
                data['hour'] = np.where(data['attributes.hour'] > 12, data['attributes.hour'] - 12, data['attributes.hour']).astype(int)
                data['minute'] = np.where(data['attributes.minute'] == 0, "00", data['attributes.minute'])
                data['Event Time'] = data['hour'].astype(str) + ":" + data['minute'].astype(str)
                return data.groupby(['Headcount Type', 'Date', 'Event Time'])['Headcounts'].sum().reset_index()
        hc_trend_df = headcounts_trend(st.session_state.headcounts_df)

        headcount_col, giving_col = st.columns(2)
        
        with headcount_col.container(border=True):
                st.subheader("Headcount Metrics")
                times = np.sort(pd.unique(hc_trend_df['Event Time']))
                selection = st.pills("Event Times", times, selection_mode="multi", default=times)
                trend_tab, yoy_tab = st.tabs(['Trend', 'Year / Year'])
                trend_tab.bar_chart(data=hc_trend_df[hc_trend_df['Event Time'].isin(selection)], x='Date', y='Headcounts', x_label='Date', y_label='Headcounts', color='Headcount Type',)# horizontal=False, stack=None, width=None, height=None, use_container_width=True)
                st.write(hc_trend_df)
                st.write(st.session_state.headcounts_df)
                
        with giving_col.container(border=True):
                st.subheader("Giving Metrics")
