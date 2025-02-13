import streamlit as st
from streamlit_oauth import OAuth2Component
from utils.auth import pcoAuth
import pypco

from PIL import Image
# Loading Image using PIL
im = Image.open('/planning_center_ai/utils/dl_dark_logo.png')


st.set_page_config(page_title="Planning Center Analytics App", layout="wide", page_icon  = im)

st.image("https://media.licdn.com/dms/image/v2/D4E16AQGCrog5mV8nBQ/profile-displaybackgroundimage-shrink_350_1400/B4EZUAA8ZzHgAY-/0/1739462002589?e=1744848000&v=beta&t=miQyzZN82YjcYs9B_Mc-UVhaKt01dqVnPE56CnaVPbw",
        width = 250)
st.title("Planning Center Analytics")



#with st.sidebar:
#  pcoAuth()

if 'token' not in st.session_state:
  st.write('Please authorize our app to access your Planning Center data.')
  pcoAuth()
else:
  # Once you've gotten your access token, you can initialize a pypco object like this:
  pco = pypco.PCO(token=st.session_state.token['access_token'])
  
  # Now, you're ready to go.
  # The iterate() function provides an easy way to retrieve lists of objects
  # from an API endpoint, and automatically handles pagination
  people = pco.iterate('/people/v2/people?include=addresses,emails,field_data,households,inactive_reason,marital_status,organization,phone_numbers,primary_campus')
  person = next(people)
  
  st.write(people)
  
