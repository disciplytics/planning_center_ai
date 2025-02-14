import streamlit as st
from streamlit_oauth import OAuth2Component
from utils.auth import pcoAuth
import pypco
import pandas as pd
import asyncio


st.set_page_config(page_title="Planning Center Analytics App", layout="wide")

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
  
  async def fetch_people_data():
          people_df = []
          for person in pco.iterate('/people/v2/people?include=addresses,emails,field_data,households,inactive_reason,marital_status,organization,phone_numbers,primary_campus'):
               people_df.append(person)
    return people_df

  async def fetch_households_data():
          households_df = []
          for household in pco.iterate('/people/v2/households?include=people'):
               households_df.append(household)
    return households_df

   async def main():
     await fetch_people_data()
     await fetch_households_data()

if __name__ == "__main__":
    asyncio.run(main())
  
st.json(people_df)
st.json(households_df)
#st.dataframe(pd.json_normalize(people_df))

  
