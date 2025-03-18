import streamlit as st

login_page = st.Page(
  'pages/login.py', 
  title = 'Login', 
  icon=":material/login:", 
  default=True
)

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
  default=False
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
            "": [login_page],
            "Reports": [church_analytics, household_health_monitor],
            "Integrations": [pco_integration],
          
        }
    )

pg.run()
