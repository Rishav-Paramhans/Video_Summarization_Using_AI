from haystack import component, Pipeline
import whisper
from pytube import YouTube
#from haystack.document_stores import InMemoryDocumentStore
from haystack import Document
from io import BytesIO
from moviepy.editor import AudioFileClip
import os
import yt_dlp
from pydub import AudioSegment

# Define the WhisperTranslator component
@component
class WhisperTranslator:
    """
    A component to translate as well as transcribe the audio data
    """
    @component.output_types(translated_text=dict)
    def run(self, input_audio:BytesIO):
        # Load the Whisper model
        model = whisper.load_model("base")
        # Convert BytesIO to a format Whisper can process
        audio_segment = AudioSegment.from_file(input_audio, format="mp3")
        
        # Export audio segment to a temporary file
        temp_audio_path = "temp_audio.wav"
        audio_segment.export(temp_audio_path, format="wav")
        # Transcribe and translate the audio file
        result = model.transcribe(temp_audio_path, task="translate")
        
        # Return the translated text
        return result

@component
class AudioExtractor:
    """_summary_: A component to download video from youtube and extracts audio
    """
    @component.output_types(extracted_audio= BytesIO)
    def run(self, url:str):
        try:
            # Use yt-dlp to download audio
            ydl_opts = {
                'format': 'bestaudio/best',
                'extractaudio': True,  # Download audio only
                'audioformat': 'mp3',  # Save as mp3
                'outtmpl': 'temp_audio.mp3',  # Output file path
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Read the downloaded audio file into BytesIO
            with open('temp_audio.mp3', 'rb') as f:
                audio_data = BytesIO(f.read())
            # Clean up the temporary file
            os.remove('temp_audio.mp3')
            return {"extracted_audio": audio_data}
        
        except Exception as e:
            print(f"Error extracting audio: {e}")
            return {"extracted_audio": None}


if __name__ == "__main__":
    # Create the pipeline
    pipeline = Pipeline()

    # Input audio file path
    input_video_url = "https://www.youtube.com/watch?v=1ZwXkw9_Xq8"
    
    # Add the WhisperTranslator component to the pipeline
    audio_extractor = AudioExtractor()
    whisper_translator = WhisperTranslator()
    pipeline.add_component(name="audio_extractor", instance=audio_extractor)
    pipeline.add_component(name="whisper_translator", instance= whisper_translator)

    pipeline.connect("audio_extractor","whisper_translator" )
    #pipeline.draw(path=r"./local_path.png")
    # Run the pipeline
    result = pipeline.run({"url": input_video_url})
    print(result)
    print(result["whisper_translator"]["text"])