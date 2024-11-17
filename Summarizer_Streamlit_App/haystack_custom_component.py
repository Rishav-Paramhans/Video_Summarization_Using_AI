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
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import pipeline as hfpipeline
from utils import sliding_window
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
# Define the WhisperTranslator component
@component
class WhisperTranslator:
    """
    A component to translate as well as transcribe the audio data
    """
    @component.output_types(translated_text=dict)
    def run(self, extracted_audio_path:str):
        print("Translator started")
        device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load the Whisper model
        model = whisper.load_model("base")
        extracted_audio_path= extracted_audio_path.replace("\\", r"/")
        extracted_audio_path= extracted_audio_path.replace(" ", r"")
        extracted_audio_path = r"{}".format(extracted_audio_path)

        translated_text = model.transcribe(extracted_audio_path, task="translate")
        
        return {"translated_text": translated_text}

@component
class AudioExtractor:
    """_summary_: A component to download video from youtube and extracts audio
    """
    @component.output_types(extracted_audio_path= str)
    def run(self, url:str):
        try:
            print("Audo extarctor started")
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
                #print("audio file path", audio_file_path)
            return {"extracted_audio_path": audio_file_path}
        except Exception as e:
            print(f"Error extracting audio: {e}")
            return {"extracted_audio_path":None}

@component
class Summarizer:
    """_summary_: A component which takes in the transcript/english-translated text and summarizes it
    """
    @component.output_types(summary= str)
    def run(self, translated_text:dict):
        """_summary_

        Args:
            translated_text (str): _description_
        """


        # Load the model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained("DISLab/SummLlama3.2-3B")
        model = AutoModelForCausalLM.from_pretrained("DISLab/SummLlama3.2-3B")

        # Check if CUDA is available and move model to the appropriate device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)  # Move the model to GPU or CPU

        # Define the input (assuming 'translated_text' is a dictionary with a 'text' key)
        #input_text = f"Summarize the input text in 250 words: Input: {translated_text['text']}, Summary"
        input_text = (
            f"Summarize the following input text in up to 250 words, organized as a bulleted list "
            f"with up to 10 key points. Ensure each point is concise and informative. "
            f"Input text: {translated_text['text']}"
            f"Summary:"
        )

        # Tokenize the input text and move the tokenized tensors to the correct device
        inputs = tokenizer(input_text, return_tensors="pt")
        inputs = {key: value.to(device) for key, value in inputs.items()}  # Move inputs to the same device as the model

        # Generate output using the model
        output_ids = model.generate(
            inputs["input_ids"],  # Use input_ids from tokenized inputs
            max_new_tokens=250,  # Control the length of the summary
            num_beams=5,  # Beam search for better output quality
            early_stopping=True  # Stop early when the output seems complete
        )

        # Decode the generated output into human-readable text
        output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        # Print the generated summary (optional for debugging)
        print("Generated Summary:")
        print(output_text)

        # Return the generated summary
        return {"summary": output_text}


@component
class Summarizer2:
    """_summary_: A component which takes in the transcript/english-translated text and summarizes it
    """
    @component.output_types(summary= str)
    def run(self, translated_text:dict):
        """_summary_

        Args:
            translated_text (str): _description_
        """
        # Load model directly
        print("Summarizer initiated")

        #model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
        #tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
        #model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large")
        #tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")

        #tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
        #model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

        

        tokenizer = AutoTokenizer.from_pretrained("allenai/led-large-16384")
        model = AutoModelForSeq2SeqLM.from_pretrained("allenai/led-large-16384")

        print("translated text: ", translated_text["text"])
        # Tokenize input with larger context window
        input_text = r"Summarize the following text in five bullet points: ".format(translated_text["text"])
        inputs = tokenizer(input_text, return_tensors="pt", max_length=32000, truncation=True)

        # Generate summary using the model
        output = model.generate(**inputs, max_new_tokens=1024)
        summary = tokenizer.decode(output[0], skip_special_tokens=True)
                
        print(summary)
        return {"summary": summary}




if __name__ == "__main__":
    # Create the pipeline
    pipeline = Pipeline()

    # Input audio file path
    input_video_url = "https://www.youtube.com/shorts/DLF3Ky5UZlg"
    
    # Add the WhisperTranslator component to the pipeline
    audio_extractor = AudioExtractor()
    whisper_translator = WhisperTranslator()
    summarizer = Summarizer()
    pipeline.add_component(name="audio_extractor", instance=audio_extractor)
    pipeline.add_component(name="whisper_translator", instance= whisper_translator)
    pipeline.add_component(name="summarizer", instance=summarizer)
    pipeline.connect("audio_extractor.extracted_audio_path", "whisper_translator.extracted_audio_path")
    pipeline.connect("whisper_translator.translated_text", "summarizer.translated_text")
    #pipeline.draw(path=r"./assets/Summarisation_Pipeline.png")
    print(pipeline)
    # Run the pipeline
    result = pipeline.run({"url": input_video_url})
    #print("Final pipeline result:", result)
    print("result", result)