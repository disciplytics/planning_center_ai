import streamlit as st

pco_integration = st.Page(
  'pages/pco_integration.py', 
  title = 'Planning Center Integration', 
  icon=":material/sync:", 
  default=False
)


church_analytics = st.Page(
  'pages/church_analytics.py', 
  title = 'Church Analytics', 
  icon=":material/monitoring:", 
  default=True
)

household_health_monitor = st.Page(
  'pages/household_health_monitor.py', 
  title = 'Household Health Monitor', 
  icon=":material/ecg_heart:", 
  default=False
)

# navigation 
pg = st.navigation(
        {
            #"Home": [],
            "Analytics": [church_analytics, household_health_monitor],
            "Integrations": [pco_integration],
          
        }
    )

pg.run()
