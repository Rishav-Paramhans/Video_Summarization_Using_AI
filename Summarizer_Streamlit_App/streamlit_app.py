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

def main():
    make_sidebar()

    st.title("Welcome to your Personalised LLM powered Yotube Video Summarizer")

    st.write("Please log in to continue (username `admin`, password `2311t`).")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log in", type="primary"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            sleep(0.5)
            st.switch_page("pages/page1.py")
        else:
            st.error("Incorrect username or password")


if __name__ == "__main__":

    main()
