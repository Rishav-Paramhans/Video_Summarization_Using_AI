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
# Define the WhisperTranslator component
@component
class WhisperTranslator:
    """
    A component to translate as well as transcribe the audio data
    """
    @component.output_types(translated_text=dict)
    def run(self, extracted_audio_path:str):
        # Load the Whisper model
        model = whisper.load_model("base")
        extracted_audio_path= extracted_audio_path.replace("\\", r"/")
        extracted_audio_path= extracted_audio_path.replace(" ", r"")
        extracted_audio_path = r"{}".format(extracted_audio_path)
        result = model.transcribe(extracted_audio_path, task="translate")
        return result

@component
class AudioExtractor:
    """_summary_: A component to download video from youtube and extracts audio
    """
    @component.output_types(extracted_audio_path= str)
    def run(self, url:str):
        try:
            # Setup options for yt-dlp
            ydl_opts = {
                'format': 'bestaudio/best',
                'extractaudio': True,  # Download audio only
                'audioformat': 'mp3',  # Save as mp3
                'outtmpl': 'temp.mp3',  # Output file path with title as name
            }

            # Use yt-dlp to download audio and extract metadata (e.g., title)
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                
                audio_file_name = 'temp.mp3'

                audio_file_path = os.path.abspath(audio_file_name)  # Get the absolute path
                print("audio file path", audio_file_path)
            return {"extracted_audio_path": audio_file_path}
        except Exception as e:
            print(f"Error extracting audio: {e}")
            return {"extracted_audio_path":None}


if __name__ == "__main__":
    # Create the pipeline
    pipeline = Pipeline()

    # Input audio file path
    input_video_url = "https://www.youtube.com/watch?v=vJNjaaylllY"
    
    # Add the WhisperTranslator component to the pipeline
    audio_extractor = AudioExtractor()
    whisper_translator = WhisperTranslator()
    pipeline.add_component(name="audio_extractor", instance=audio_extractor)
    pipeline.add_component(name="whisper_translator", instance= whisper_translator)

    pipeline.connect("audio_extractor","whisper_translator")
    #pipeline.draw(path=r"./local_path.png")
    # Run the pipeline
    result = pipeline.run({"url": input_video_url})

    print(result["whisper_translator"]["text"])