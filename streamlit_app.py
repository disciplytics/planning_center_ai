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

# navigation 
pg = st.navigation(
        {
            #"Home": [],
            "Analytics": [church_analytics],
            "Integrations": [pco_integration],
          
        }
    )

pg.run()
