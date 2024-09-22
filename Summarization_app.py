import streamlit as st
from haystack import Pipeline
from Summarization_pipeline import summarization_pipeline  # Import your Haystack pipeline
import requests

import streamlit as st
from haystack_custom_component import CustomPipeline

# Example user credentials for authentication
USER_CREDENTIALS = {
    "username": "admin",
    "password": "admin123"
}

# Function to authenticate users
def authenticate(username, password):
    return username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']

# Streamlit App
def main():
    st.title("Video Summarization App")

    # Define session state for login status
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # If the user is not logged in, show the login form
    if not st.session_state['logged_in']:
        st.subheader("Please log in")

        # Create a form for user login
        with st.form("Login Form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")

        # Check login details
        if login_button:
            if authenticate(username, password):
                st.success("Logged in successfully!")
                st.session_state['logged_in'] = True
            else:
                st.error("Invalid username or password")

    # If the user is logged in, show the input for YouTube URL
    if st.session_state['logged_in']:
        st.subheader("Enter the YouTube URL to summarize")
        
        # Create a form for entering the YouTube URL
        with st.form("URL Form"):
            youtube_url = st.text_input("YouTube URL")
            submit_button = st.form_submit_button("Summarize")

        # When the user submits the URL, run the summarization pipeline
        if submit_button and youtube_url:
            st.write("Summarizing video...")

            # Replace this with your pipeline's run method
            #pipeline = CustomPipeline()  # Assuming your Haystack pipeline is in `CustomPipeline`
            try:
                result = summarization_pipeline .run({"url": youtube_url})
                summary = result["summary"]

                # Show the result summary
                st.subheader("Summary of the Video:")
                st.write(summary)
            except Exception as e:
                st.error(f"Error occurred during summarization: {e}")

if __name__ == "__main__":
    main()
