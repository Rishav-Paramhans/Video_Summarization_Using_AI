import streamlit as st
import requests  # For fetching the video thumbnail
#from summarization_pipeline import summarization_pipeline  # Import your Haystack pipeline
from streamlit_extras.switch_page_button import switch_page

# Example user credentials for authentication
USER_CREDENTIALS = {
    "username": "admin",
    "password": "Vit_Academeics12345#"
}
# Function to authenticate users
def authenticate(username, password):
    return username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']

# Function to get video thumbnail
def get_video_thumbnail(url):
    video_id = url.split("v=")[-1]
    return f"https://img.youtube.com/vi/{video_id}/0.jpg"

# Main function
def main():
    # Set up session state for login
    
    
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'  # Default page is login

    # Show login page if the user is not logged in
    if st.session_state['page'] == 'login':
        st.title("Video Summarization App - Login")
        st.subheader("Please log in to access the dashboard")

        # Login form
        with st.form("Login Form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")

        # Authenticate the user
        if login_button:
            if authenticate(username, password):
                st.success("Logged in successfully!")
                st.session_state['logged_in'] = True
                

                switch_page("dashboard")
                st.session_state['page'] = 'dashboard'  # Redirect to dashboard

            else:
                st.error("Invalid username or password")

                # Show dashboard page after successful login
        if st.session_state['logged_in'] and st.session_state['page'] == 'dashboard':
            st.title("Video Summarization Dashboard")
            st.subheader("Enter the YouTube URL to summarize")

            # Form to enter YouTube URL
            with st.form("URL Form"):
                youtube_url = st.text_input("YouTube URL")
                submit_button = st.form_submit_button("Submit")
            #Only store the URL in session state if the form is submitted
            if submit_button:
                st.session_state['youtube_url'] = youtube_url
                    # Only proceed to show thumbnail and allow summarization after URL is submitted
            # Only proceed to show thumbnail and allow summarization after URL is submitted and stored
            if 'youtube_url' in st.session_state and st.session_state['youtube_url']:
                st.write("Video Thumbnail")
                # Display video thumbnail
                thumbnail_url = get_video_thumbnail(st.session_state['youtube_url'])
                st.image(thumbnail_url, caption="Video Thumbnail", use_column_width=True)

if __name__ == "__main__":
    main()
