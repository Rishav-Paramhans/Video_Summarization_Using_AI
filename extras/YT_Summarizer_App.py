import streamlit as st
from pytube import YouTube
from haystack.nodes import PromptModel, PromptNode
from haystack.nodes.audio import WhisperTranscriber, WhisperModel
from haystack.pipelines import Pipeline
import time












if __name__ == "__main__":
    # Initialize the WhisperTranscriber and specify the task as "translate"
    whisper_transcriber = WhisperModel(task="translate")

    # Create a Haystack pipeline for transcription and translation
    pipeline = Pipeline()
    pipeline.add_node(component=whisper_transcriber, name="whisper_transcriber", inputs=["query"])

    # Path to the audio file (non-English audio)
    audio_path = r"D:/Python_Projects/Video_Summarization_Using_AI\BJP जीते या CONGRESS ( इन शेयर्स को Long Term में कोई भी फर्क नहीं पड़ेगा )🔴 Election 2024🔴 SMKC.webm"

    # Run the pipeline to get transcription and translation into English
    transcription_result = pipeline.run(file_path=audio_path)
    english_translation = transcription_result["documents"][0].content

    print("Translated Text in English:", english_translation)
