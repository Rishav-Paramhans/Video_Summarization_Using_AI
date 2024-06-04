import streamlit as st
from pytube import YouTube
from haystack.nodes import PromptModel, PromptNode

# Haystack provides two implemenatations for this class whisper tranbscribers:
# 1. Through API, 2. Local implemenattaion (here I will be using local implementation)
from haystack.nodes.audio import WhisperTranscriber
from haystack.pipelines import Pipeline
import time
import logging
# from model_add import LlamaCPPInvocationLayer

def download_video(url):
        yt = YouTube(url)
        video = yt.streams.filter(abr="160kbps").last()

def intialize_model(model_path):
    """_summary_: Function in the video uses the llama cpp layer for invocation

    Args:
        model_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    return PromptModel(model_name_or_path= model_path, use_gpu= True,
                         max_length= 512)

def initialize_prompt_node(model):
     summary =  "deepset/summarizaiton"
     return PromptNode(model_name_or_path= model, default_prompt_template= summary, use_gpu= True)

def transcribe_audio(file_path,  prompt_node):
     whisper = WhisperTranscriber() #if i dont give th api key, it takes the local implementation
     pipeline = Pipeline()
     pipeline.add_node(component= whisper, name="whisper", inputs=["File"])
     pipeline.add_node(component= prompt_node, name="prompt", inputs=["whisper"])
     output = pipeline.run(file_paths=[file_path])
     return output

     


if __name__ == "__main__":
    st.set_page_config(
        layout= "wide",
        page_icon= "Yotube Summary Generator"

    )

    st.title("Yotube Video Summarizer")
    st.markdown('<style>h1{color:orange; text-align:center;}</style>', unsafe_allow_html=True)
    st.subheader("Build with llam3, Whisper, Haystack, Streamlit and love")
    st.markdown('<style>h3{color:pink; text-align:center;}</style>', unsafe_allow_html=True)


    with st.expander("About the App:"):
         st.write("This app allows you to summarizer the youtube video ")
         st.write("Enter a Youtube video URL and click on Submut button")

    youtube_url = st.text_input("Yotuve video URL")

    if st.button("Submit") and youtube_url:
         file_path = download_video(youtube_url)
         model_path = "llama-2-7b"
         model = intialize_model(model_path=model_path)
         prompt_node = initialize_prompt_node(model)
         output = transcribe_audio(file_path=file_path, prompt_node=prompt_node)


         col1, col2 = st.colums([1,1])

         with col1:
              st.video(youtube_url)
         with col2:
              st.header("Summarization of the video")
              st.write(output)
              st.success(output["results"][0].spli("\n\n[INST]")[0])
            
        # to run this streamlit run YT_Summary_Generator.py
              




    
