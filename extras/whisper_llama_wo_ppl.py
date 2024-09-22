import whisper
import os
os.environ['PATH'] += os.pathsep + r'C:\ffmpeg\bin'
from pytube import YouTube
import torch
import whisper
from haystack.nodes.audio import WhisperTranscriber
from haystack import Document
from haystack.nodes import TransformersTranslator
import os
#from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoModelForCausalLM,AutoModel
from haystack import Pipeline
from haystack.nodes import BaseComponent
from haystack.nodes import PromptModel, PromptNode
from ctransformers import AutoModelForCausalLM, AutoTokenizer



if __name__ =="__main__":

    # Verify the path
    print(os.environ['PATH'])

    # Check the available models
    available_models = whisper.available_models()
    print("Available Whisper models:", available_models)

    # Load the desired model
    model = whisper.load_model("large")

    # Verify the model is loaded
    print("Whisper model loaded successfully:", model)

    # Path to the audio file
    audio_file_path = r"D:/Python_Projects/Video_Summarization_Using_AI/Gemini LLM JSON Mode Generate Structured Output from LLM.webm"

    # Check if the file exists
    if not os.path.exists(audio_file_path):
        print(f"Audio file '{audio_file_path}' does not exist.")
    else:
        # Transcribe the audio file
        result = model.transcribe(audio_file_path)

        # Print the transcription
        print("Transcription:")
        print(result["text"])


    """
    model_name_or_path = "meta-llama/Llama-2-7b-chat-hf"
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_name_or_path, trust_remote_code=True)
    #model = AutoModelForSeq2SeqLM.from_pretrained(model_name_or_path)
    #tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    inputs = tokenizer(result["text"], return_tensors="pt", max_length=1024, truncation=True)

    # Generate summary using Llama-2 model
    summary_ids = model.generate(inputs["input_ids"].to(device), max_new_tokens=1024, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Print the summary
    print("Summary:")
    print(summary)
    """
    # Initialize the LLaMA-2 model with transformers
    llama_model = AutoModelForCausalLM.from_pretrained("marella/gpt-2-ggml", hf=True)
    llama_tokenizer = AutoTokenizer.from_pretrained(llama_model)

    # Prepare the input text for the model
    input_text = result["text"]
    inputs = llama_tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    inputs = {key: value.to(device) for key, value in inputs.items()}
    llama_model.to(device)

    # Generate summary using the LLaMA-2 model
    summary_ids = llama_model.generate(inputs["input_ids"], max_new_tokens=1024, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = llama_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # Print the summary
    print("Summary:")
    print(summary)
    




