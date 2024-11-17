import torch.cuda
from navigation import make_sidebar
import streamlit as st
import time
import sys
import os
from Summarization_pipeline import summarization_pipeline

def main():
    device = "cuda" if torch.cuda.is_available() else 'cpu'
    
    make_sidebar()
    # Set the title and background color
    st.title("YouTube Video Summarizer 🎥")
    st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)
    st.subheader('Built with the Llama 3.2 🦙, Haystack, Streamlit')
    st.markdown('<style>h3{color: pink;  text-align: center;}</style>', unsafe_allow_html=True)

    # Expander for app details
    with st.expander("About the App"):
        st.write("Your personal Youtube Video Summarizer- Fully Open Source")
        st.write("Enter a YouTube URL in the input box below and click 'Submit' to start. This app is built by Rishav to"
                 " increase productivity")

    # Input box for YouTube URL
    youtube_url = st.text_input("Enter YouTube URL")

    # Submit button
    if st.button("Submit") and youtube_url:
        start_time = time.time()  # Start the timer
        output = summarization_pipeline.run({"url": youtube_url})
        print("output", output)
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time

        # Display layout with 2 columns
        col1, col2 = st.columns([1,1])

        # Column 1: Video view
        with col1:
            st.video(youtube_url)

        # Column 2: Summary View
        with col2:
            st.header("Summarization of YouTube Video")
            st.write(output["summarizer"]["summary"])
            #st.success(output["summarizer"][0].split("\n\n[INST]")[0])
            st.write(f"Time taken: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()