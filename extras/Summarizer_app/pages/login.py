
import streamlit as st
from time import sleep
from navigation import make_sidebar

# Example user credentials for authentication
USER_CREDENTIALS = {
    "username": "admin",
    "password": "Vit_Academeics12345#"
}
# Function to authenticate users
def authenticate(username, password):
    return username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']



make_sidebar()

st.title("Your Youtube Video Summarizer")

st.write("Please log in to continue (username `test`, password `test`).")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Log in", type="primary"):
    if authenticate(username, password):
        st.success("Logged in successfully!")
        st.session_state["logged_in"] = True
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("./pages/dashboard.py")
    else:
        st.error("Incorrect username or password")