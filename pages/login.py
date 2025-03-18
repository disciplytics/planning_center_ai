import streamlit as st
from st_paywall import add_auth

    
# PAGE CONGIG
st.set_page_config(
        page_title="Login", 
        layout="wide",
        page_icon = 'https://jimdo-storage.freetls.fastly.net/image/446612637/7c401e7a-6b6d-4ec8-84a5-4ab2cae82c9e.png?quality=80,90&auto=webp&disable=upscale&width=1024&height=576&trim=0,0,0,0',
)

# LOGO
st.image("https://media.licdn.com/dms/image/v2/D4E16AQGCrog5mV8nBQ/profile-displaybackgroundimage-shrink_350_1400/B4EZUAA8ZzHgAY-/0/1739462002589?e=1744848000&v=beta&t=miQyzZN82YjcYs9B_Mc-UVhaKt01dqVnPE56CnaVPbw",
        width = 250)

# Handle Streamlit's native authentication
if not st.experimental_user.is_logged_in:
    if st.button("Log in using Streamlit's native authentication"):
        st.login()
else:
    # Add subscription check for logged-in users
    add_auth(required=True)
    
    # Your app code here - only runs for subscribed users
    st.write('Stuff')

    if st.button("Log out"):
            st.logout()
