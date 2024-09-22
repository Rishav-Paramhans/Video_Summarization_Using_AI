import streamlit as st
from haystack import Pipeline
from Summarization_pipeline import summarization_pipeline  # Import your Haystack pipeline
import requests


# Example user credentials for authentication
USER_CREDENTIALS = {
    "username": "admin",
    "password": "admin123"
}

# Function to authenticate users
def authenticate(username, password):
    return username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']
# Function to get video thumbnail
def get_video_thumbnail(url):
    video_id = url.split("v=")[-1]
    return f"https://img.youtube.com/vi/{video_id}/0.jpg"
def main():
    # Define session state for login status
    st.session_state['logged_in'] = False

    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'  # Default to login page

    st.title("Video Summarization App")
    st.markdown('<style>h1{color:orange;text-align:center;}</style>', unsafe_allow_html=True)
    st.subheader("Your personal app to summarize anything on YouTube")
    st.markdown('<style>h3{color:pink;text-align:center;}</style>', unsafe_allow_html=True)

    st.session_state['logged_in'] = False
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'  # Default to login page

    # Title and description
    st.title("Video Summarization App")
    st.markdown('<style>h1{color:orange;text-align:center;}</style>', unsafe_allow_html=True)

    if st.session_state['page'] == 'login':
        # Login form
        st.subheader("Please log in")
        with st.form("Login Form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")

        # Check login details
        if login_button:
            if authenticate(username, password):
                st.success("Logged in successfully!")
                st.session_state['logged_in'] = True
                st.session_state['page'] = 'dashboard'  # Navigate to dashboard
            else:
                st.error("Invalid username or password")

    elif st.session_state['page'] == 'dashboard':
        st.title("Video Summarization App")
        st.markdown('<style>h1{color:orange;text-align:center;}</style>', unsafe_allow_html=True)
        st.subheader("Your personal app to summarize anything on YouTube")
        st.markdown('<style>h3{color:pink;text-align:center;}</style>', unsafe_allow_html=True)
        # Dashboard page
        st.subheader("Dashboard: Enter the YouTube URL to summarize")
        youtube_url = st.text_input("YouTube URL")

        if youtube_url:
            # Display video thumbnail
            thumbnail_url = get_video_thumbnail(youtube_url)
            st.image(thumbnail_url, caption="Video Thumbnail", use_column_width=True)

            # Summarization button
            if st.button("Summarize"):
                st.write("Summarizing video...")
                try:
                    result = summarization_pipeline.run({"url": youtube_url})
                    summary = result["summary"]

                    # Show the result summary
                    st.subheader("Summary of the Video:")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error occurred during summarization: {e}")

if __name__ == "__main__":
    main()
    
    
    

if __name__ == "__main__":
    main()
