import streamlit as st

# PAGE CONGIG
#st.set_page_config(
#        page_title="Planning Center Analytics", 
#        layout="wide",
#        page_icon = 'https://jimdo-storage.freetls.fastly.net/image/446612637/7c401e7a-6b6d-4ec8-84a5-4ab2cae82c9e.png?quality=80,90&auto=webp&disable=upscale&width=1024&height=576&trim=0,0,0,0',
#)

# LOGO
#st.image("https://media.licdn.com/dms/image/v2/D4E16AQGCrog5mV8nBQ/profile-displaybackgroundimage-shrink_350_1400/B4EZUAA8ZzHgAY-/0/1739462002589?e=1744848000&v=beta&t=miQyzZN82YjcYs9B_Mc-UVhaKt01dqVnPE56CnaVPbw",
#        width = 250)

# PAGE TITLE
#st.title("Planning Center Analytics :church:")

pco_integration = st.Page(
  'pages/pco_integration.py', 
  title = 'Planning Center Integration', 
  icon=":material/sync:", 
  default=True
)


# navigation 
pg = st.navigation(
        {
            "Planning Center Integration": [pco_integration],

        }
    )

pg.run()
