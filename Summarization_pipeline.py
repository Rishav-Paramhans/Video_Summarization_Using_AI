from haystack import component, Pipeline
import whisper
from pytube import YouTube
#from haystack.document_stores import InMemoryDocumentStore
from haystack import Document
from io import BytesIO
from moviepy.editor import AudioFileClip
import os
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import re
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel,  AutoModelForSeq2SeqLM
from llama_cpp import Llama
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import pipeline as hfpipeline
from haystack_custom_component import *





# Create the pipeline
summarization_pipeline = Pipeline()

# Input audio file path
input_video_url = "https://www.youtube.com/watch?v=vJNjaaylllY"
    
# Add the WhisperTranslator component to the pipeline
audio_extractor = AudioExtractor()
whisper_translator = WhisperTranslator()
summarizer = Summarizer()
summarization_pipeline.add_component(name="audio_extractor", instance=audio_extractor)
summarization_pipeline.add_component(name="whisper_translator", instance= whisper_translator)
summarization_pipeline.add_component(name="summarizer", instance=summarizer)
summarization_pipeline.connect("audio_extractor.extracted_audio_path", "whisper_translator.extracted_audio_path")
summarization_pipeline.connect("whisper_translator.translated_text", "summarizer.translated_text")
summarization_pipeline.draw(path=r"./assets/Summarisation_Pipeline.png")
print(summarization_pipeline)
# Run the pipeline
result = summarization_pipeline.run({"url": input_video_url})
#print("Final pipeline result:", result)
print("result", result)