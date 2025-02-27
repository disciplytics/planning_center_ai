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
                data['Week of Year'] = pd.to_datetime(data['attributes.starts_at'], utc=True).dt.isocalendar().week
                data['Year'] = pd.to_datetime(data['attributes.starts_at'], utc=True).dt.year.astype(str)
                data['hour'] = np.where(data['attributes.hour'] > 12, data['attributes.hour'] - 12, data['attributes.hour']).astype(int)
                data['minute'] = np.where(data['attributes.minute'] == 0, "00", data['attributes.minute'].astype(int).astype(str))
                data['Event Time'] = data['hour'].astype(str) + ":" + data['minute'].astype(str)
                return data.groupby(['Headcount Type', 'Week of Year', 'Year', 'Date', 'Event Time'])[['Headcounts', 'Guest Count', 'Regular Count', 'Volunteer Count']].sum().reset_index()
        hc_trend_df = headcounts_data(st.session_state.headcounts_df)

        def headcounts_analysis(data, metric):
                trend_tab.bar_chart(
                        data=data[(data['Event Time'].isin(timeSelection)) & (data['Headcount Type'].isin(headcountTypes)) & (data['Year'].isin(yearSelection))].groupby(['Date', 'Headcount Type'])[metric].sum().reset_index(), 
                        x='Date', 
                        y=metric, 
                        x_label='Date', 
                        y_label=metric, 
                        color='Headcount Type',)
                
                yoy_tab.line_chart(
                        data=data[(data['Event Time'].isin(timeSelection)) & (data['Headcount Type'].isin(headcountTypes)) & (data['Year'].isin(yearSelection))].groupby(['Year', 'Week of Year'])[metric].sum().reset_index(), 
                        x='Week of Year', 
                        y=metric, 
                        x_label='Week of Year', 
                        y_label=metric, 
                        color='Year',)
                
        
        with st.container(border=True):
                st.subheader("Headcount Metrics")

                years = np.sort(pd.unique(hc_trend_df['Year']))
                times = np.sort(pd.unique(hc_trend_df['Event Time']))
                types = np.sort(pd.unique(hc_trend_df['Headcount Type']))
                metrics = ['Headcounts', 'Guest Count', 'Regular Count', 'Volunteer Count']
                
                with st.expander("Filters", icon=":material/filter_alt:"):
                        col1, col2, col3, col4 = st.columns(4)
                        metricTypes = col1.pills("Metric", metrics, selection_mode="single", default='Headcounts')
                        yearSelection = col2.pills("Year", years, selection_mode="multi", default=years)
                        timeSelection = col3.pills("Event Times", times, selection_mode="multi", default=times)
                        headcountTypes = col4.pills("Headcount Type", types, selection_mode="multi", default=types)
                        
                
                trend_tab, yoy_tab = st.tabs(['Trend', 'Year / Year'])
                headcounts_analysis(hc_trend_df, metricTypes)

        st.session_state.donations_df
        @st.cache_data
        def donations_data(data): 
                data = pd.merge(data, st.session_state.people_df[['id', 'relationships.primary_campus.data.id']], left_on = 'relationships.person.data.id', right_on = 'id')
                data = pd.merge(data, st.session_state.campus_df[['id', 'attributes.name']], left_on = 'relationships.primary_campus.data.id', right_on = 'id')
                data['Date'] = pd.to_datetime(data['attributes.received_at'], utc=True).dt.date
                data['Week of Year'] = pd.to_datetime(data['attributes.received_at'], utc=True).dt.isocalendar().week.astype(int)
                data['Year'] = pd.to_datetime(data['attributes.received_at'], utc=True).dt.year.astype(str)
                data['Month'] = pd.to_datetime(data['attributes.received_at'], utc=True).dt.month.astype(int)
                data['Donations'] = pd.to_numeric(data['attributes.amount_cents'])/100
                data['Donor Campus'] = data['attributes.name']
                data['Donation Type'] = np.where(data['relationships.recurring_donation.data'].isnull(), 'NonRecurring', 'Recurring')
                return data.groupby(['Donor Campus', 'Donation Type', 'Fund', 'Year', 'Month', 'Week of Year', 'Date'])['Donations'].sum().reset_index()
        d_trend_df = donations_data(st.session_state.donations_df)
        
        with st.container(border=True):
                st.subheader("Giving Metrics")
                years = np.sort(pd.unique(d_trend_df['Year']))
                types = np.sort(pd.unique(d_trend_df['Donation Type']))
                campuses = np.sort(pd.unique(d_trend_df['Donor Campus']))
                
                with st.expander("Filters", icon=":material/filter_alt:"):
                        col1, col2, col3 = st.columns(3)
                        yearSelection = col1.pills("Year", years, selection_mode="multi", default=years[-2:])
                        donationTypes = col2.pills("Donation Type", types, selection_mode="multi", default=types)
                        campusSelection = col3.pills("Donor Campus", campuses, selection_mode="multi", default=campuses)

                def donation_analysis(data):
                        filter_df = data[(data['Year'].isin(yearSelection)) & (data['Donation Type'].isin(donationTypes)) & (data['Donor Campus'].isin(campusSelection))]

                        yoysum, yoypct, avggift = st.columns(3)
                        # calculate metrics
                        most_recent_yr = yearSelection[-1]
                        least_recent_yr = yearSelection[-2]
                        label_val_ytd = f"YTD Giving - {most_recent_yr}"

                        max_year_week = filter_df[filter_df['Year'] == most_recent_yr]['Week of Year'].max()

                    
                        most_recent_ytd = filter_df[filter_df['Year'] == most_recent_yr]['Donations'].sum()
                        most_recent_avg = filter_df[filter_df['Year'] == most_recent_yr]['Donations'].mean()
                    
                        label_val_yoy = f"Y/Y Giving - {most_recent_yr}"
                    
                        label_val_avg = f"Average Gift - {most_recent_yr}"

                        delta_ytd = filter_df[(filter_df['Year'] == least_recent_yr) &
                                      (filter_df['Week of Year'] <= max_year_week)]['Donations'].sum()
    
                        delta_avg = filter_df[(filter_df['Year'] == least_recent_yr) &
                                      (filter_df['Week of Year'] <= max_year_week)]['Donations'].mean()

                        yoysum.metric(
                            label=label_val_ytd,
                            value= '${:,}'.format(np.round(most_recent_ytd,2)),
                            delta = f"YTD - {least_recent_yr}: {'${:,}'.format(np.round(delta_ytd/1000,2))}K",
                            delta_color="off"
                        )
                    
                        yoypct.metric(
                            label=f'{label_val_yoy}/{least_recent_yr}',
                            value= f"{np.round((most_recent_ytd - delta_ytd)/ delta_ytd * 100,2)}%",
                            delta_color="off"
                        )
                    
                        avggift.metric(
                            label=label_val_avg,
                            value= '${:,}'.format(np.round(most_recent_avg,2)),
                            delta = f"Avg Gift - {least_recent_yr}: {'${:,}'.format(np.round(delta_avg,2))}",
                            delta_color="off"
                        )
                        
                        yoyw_tab.line_chart(
                                data=filter_df.groupby(['Year', 'Week of Year'])['Donations'].sum().reset_index(), 
                                x='Week of Year', 
                                y='Donations', 
                                x_label='Week of Year', 
                                y_label='Donations', 
                                color='Year',)
                        
                        yoym_tab.line_chart(
                                data=filter_df.groupby(['Year', 'Month'])['Donations'].sum().reset_index(), 
                                x='Month', 
                                y='Donations', 
                                x_label='Month', 
                                y_label='Donations', 
                                color='Year',)
                        
                        trend_tab.bar_chart(
                                data=filter_df.groupby(['Date', 'Donor Campus'])['Donations'].sum().reset_index(), 
                                x='Date', 
                                y='Donations', 
                                x_label='Date', 
                                y_label='Donations', 
                                color='Donor Campus',)
                        
                        

                        
                        col1, col2 = st.columns(2)
                        col1.write('Donations By Fund')
                        col1.bar_chart(
                                filter_df.groupby(['Fund', 'Year'])['Donations'].sum().reset_index(), 
                                y = 'Donations', x = 'Fund', horizontal = True, color = 'Year'
                        )

                yoyw_tab, yoym_tab, trend_tab = st.tabs(['Year / Year By Week', 'Year / Year By Month', 'Trend'])
                donation_analysis(d_trend_df)

        st.session_state.people_df

        st.session_state.campus_df

        df = st.session_state.donations_df
        st.write(pd.json_normalize(df.explode('relationships.designations.data')['relationships.designations.data']))
        st.write()
