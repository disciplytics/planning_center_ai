def pcoAuth():
  from streamlit_oauth import OAuth2Component
  import streamlit as st
  
  
  # Set environment variables
  AUTHORIZE_URL = st.secrets["AUTHORIZE_URL"]
  TOKEN_URL = st.secrets["TOKEN_URL"]
  REFRESH_TOKEN_URL = st.secrets["TOKEN_URL"]
  REVOKE_TOKEN_URL = st.secrets["REVOKE_TOKEN_URL"]
  CLIENT_ID = st.secrets["PC_CLIENT_ID"]
  CLIENT_SECRET = st.secrets["PC_CLIENT_SECRET"]
  REDIRECT_URI = st.secrets["REDIRECT_URI"]
  SCOPE = st.secrets["SCOPE"]
  
  # Create OAuth2Component instance
  oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)
  
  # Check if token exists in session state
  if 'token' not in st.session_state:
      # If not, show authorize button
      result = oauth2.authorize_button("Log into Planning Center", REDIRECT_URI, SCOPE)
      if result and 'token' in result:
          # If authorization successful, save token in session state
          st.session_state.token = result.get('token')
          st.rerun()

          if st.button("Log Out"):
            del st.session_state.token
  else:
      # If token exists in session state, show the token
      token = st.session_state['token']
      st.json(token)
      if st.button("Refresh Token"):
          # If refresh token button is clicked, refresh the token
          token = oauth2.refresh_token(token)
          st.session_state.token = token
          st.rerun()

  
