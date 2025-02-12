import streamlit as st
from streamlit_oauth import OAuth2Component
from utils.auth import pcoAuth


# Set environment variables
AUTHORIZE_URL = st.secrets["AUTHORIZE_URL"]
TOKEN_URL = st.secrets["TOKEN_URL"]
REFRESH_TOKEN_URL = st.secrets["TOKEN_URL"]
REVOKE_TOKEN_URL = st.secrets["REVOKE_TOKEN_URL"]
CLIENT_ID = st.secrets["PC_CLIENT_ID"]
CLIENT_SECRET = st.secrets["PC_CLIENT_SECRET"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]
SCOPE = st.secrets["SCOPE"]

st.title("Planning Center Analytics")
with st.sidebar:
  pcoAuth()
import pypco

# Generate the login URI
#redirect_url = pypco.get_browser_redirect_url(
#    st.secrets["PC_CLIENT_ID"],
#    st.secrets["REDIRECT_URI"],
#    st.secrets["SCOPE"]
#)
# Now, you'll have the URI to which you need to send the user for authentication
# Here is where you would handle that and get back the code parameter PCO returns.

# For this example, we'll assume you've handled this and now have the code
# parameter returned from the API

# Now, we'll get the OAuth access token json response using the code we received from PCO
#token_response = pypco.get_oauth_access_token(
#    st.secrets["PC_CLIENT_ID"],
#    st.secrets["PC_CLIENT_SECRET"],
#    "<CODE_HERE>",
#    st.secrets["REDIRECT_URI"]
#)

# The response you'll receive from the get_oauth_access_token function will include your
# access token, your refresh token, and other metadata you may need later.
# You may wish/need to store this entire response on disk as securely as possible.
# Once you've gotten your access token, you can initialize a pypco object like this:
pco = pypco.PCO(token=st.session_state.token['access_token'])

# Now, you're ready to go.
# The iterate() function provides an easy way to retrieve lists of objects
# from an API endpoint, and automatically handles pagination
people = pco.iterate('/people/v2/people')
person = next(people)

st.write(people)
st.write(person)



#pco = pypco.PCO(st.session_state.token)

#st.write(pco.get('/people/v2/people'))#.get('https://api.planningcenteronline.com/people/v2/people'))
