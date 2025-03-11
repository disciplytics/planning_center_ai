import streamlit as st
from st_paywall import add_auth

st.title("🎈 Tyler's Subscription app POC 🎈")
st.balloons()

add_auth(required=True)

st.write("Congrats, you are subscribed!")
st.write('the email of the user is ' + str(st.session_state.email))


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
            "Reports": [church_analytics, household_health_monitor],
            "Integrations": [pco_integration],
          
        }
    )

pg.run()
