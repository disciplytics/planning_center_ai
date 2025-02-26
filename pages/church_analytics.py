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
        def headcounts_data(data):
                data['Headcount Type'] = data['attributes.name_at']
                data['Headcounts'] = pd.to_numeric(data['attributes.total'])
                data['Guest Count'] = pd.to_numeric(data['attributes.guest_count'])
                data['Regular Count'] = pd.to_numeric(data['attributes.regular_count'])
                data['Volunteer Count'] = pd.to_numeric(data['attributes.volunteer_count'])
                data['Date'] = pd.to_datetime(data['attributes.starts_at'], utc=True).dt.date
                data['week_of_year'] = pd.to_datetime(data['attributes.starts_at'], utc=True).dt.isocalendar().week
                data['Year'] = pd.to_datetime(data['attributes.starts_at'], utc=True).dt.year.astype(str)
                data['hour'] = np.where(data['attributes.hour'] > 12, data['attributes.hour'] - 12, data['attributes.hour']).astype(int)
                data['minute'] = np.where(data['attributes.minute'] == 0, "00", data['attributes.minute'].astype(int).astype(str))
                data['Event Time'] = data['hour'].astype(str) + ":" + data['minute'].astype(str)
                return data.groupby(['Headcount Type', 'week_of_year', 'Year', 'Date', 'Event Time'])[['Headcounts', 'Guest Count', 'Regular Count', 'Volunteer Count']].sum().reset_index()
        hc_trend_df = headcounts_data(st.session_state.headcounts_df)

        def headcounts_analysis(data, metric):
                trend_tab.bar_chart(
                        data=data[(data['Event Time'].isin(timeSelection)) & (data['Headcount Type'].isin(headcountTypes))].groupby(['Date', 'Headcount Type'])[metric].sum().reset_index(), 
                        x='Date', 
                        y=metric, 
                        x_label='Date', 
                        y_label=metric, 
                        color='Headcount Type',)
                
                yoy_tab.line_chart(
                        data=data[(data['Event Time'].isin(timeSelection)) & (data['Headcount Type'].isin(headcountTypes))].groupby(['Year', 'week_of_year'])[metric].sum().reset_index(), 
                        x='week_of_year', 
                        y=metric, 
                        x_label='Week of Year', 
                        y_label=metric, 
                        color='Year',)
                

        headcount_col, giving_col = st.columns(2)
        
        with headcount_col.container(border=True):
                st.subheader("Headcount Metrics")
                timeCol, hcCol, mCol = st.columns(3)
                times = np.sort(pd.unique(hc_trend_df['Event Time']))
                timeSelection = timeCol.pills("Event Times", times, selection_mode="multi", default=times)
                types = np.sort(pd.unique(hc_trend_df['Headcount Type']))
                headcountTypes = hcCol.pills("Headcount Type", types, selection_mode="multi", default=types)
                metrics = ['Headcounts', 'Guest Count', 'Regular Count', 'Volunteer Count']
                metricTypes = mCol.pills("Metric", metrics, selection_mode="single", default='Headcounts')
                
                trend_tab, yoy_tab = st.tabs(['Trend', 'Year / Year'])
                headcounts_analysis(hc_trend_df, metricTypes)
                st.write(hc_trend_df)
                st.write(st.session_state.headcounts_df)
                
        with giving_col.container(border=True):
                st.subheader("Giving Metrics")
