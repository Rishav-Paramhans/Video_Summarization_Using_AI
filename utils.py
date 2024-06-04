from pytube import YouTube
import torch
import whisper
from haystack.nodes.audio import WhisperTranscriber
from haystack import Document
from haystack.nodes import TransformersTranslator
import os
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, AutoModelForCausalLM
from haystack import Pipeline
from haystack.nodes import BaseComponent
from haystack.nodes import PromptModel, PromptNode



class WhisperTranscription(BaseComponent):
    outgoing_edges = 1
    def __init__(self, model):
        self.model = model
    
    def run(self, audio_file_path):
        result = self.model.transcribe(audio_file_path, task = "translate")
        return {"text": result["text"]}
    
    def run_batch(self, audio_file_paths):
        results = [self.run(audio_file_path) for audio_file_path in audio_file_paths]
        return results

class Summarization(BaseComponent):
    outgoing_edges = 1
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
    
    def run(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
        summary_ids = self.model.generate(inputs["input_ids"], max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return {"summary": summary}
    def run_batch(self, texts):
        summaries = []
        for text in texts:
            result = self.run(text)
            summaries.append(result["summary"])
        return {"summaries": summaries}



def download_youtube_video(video_url, output_path='.'):
    """_summary_: Downloads a youtube video using the url

    Args:
        video_url (_type_): _description_: data type <str>
        output_path (str, optional): _description_. Defaults to '.': data type <str>.
    """
    try:
        # Create a YouTube object
        yt = YouTube(video_url)
        
        # Get the highest resolution stream
        stream = yt.streams.filter(only_audio=True).last()
        
        # Download the video
        print(f"Downloading '{yt.title}'...")
        stream.download(output_path=output_path)
        print(f"Download completed! Video saved to '{output_path}'")
        
    except Exception as e:
        print(f"An error occurred: {e}") 
    return (yt.title + ".webm")

def intialize_model(model_name_or_path):
    """_summary_: Function in the video uses the llama cpp layer for invocation

    Args:
        model_path (_type_): _description_

    Returns:
        _type_: _description_

    """
    tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_name_or_path, trust_remote_code=True)
    #model = AutoModelForSeq2SeqLM.from_pretrained(model_name_or_path)
    #tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
    return PromptModel(model_name_or_path= model_name_or_path, use_gpu= True,
                         max_length= 512)
def transcribe_audio(file_path, prompt_node):
    whisper_model = whisper.load_model("large")  # Make sure to load your Whisper model correctly
    whisper = WhisperTranscription(whisper_model)
    pipeline = Pipeline()
    pipeline.add_node(component=whisper, name="whisper", inputs=["File"])
    pipeline.add_node(component=prompt_node, name="prompt", inputs=["whisper"])
    output = pipeline.run(file_paths=[file_path])
    return output


def initialize_prompt_node(model):
        summary =  "deepset/summarizaiton"
        return PromptNode(model_name_or_path= model, default_prompt_template= summary, use_gpu= True)


if __name__ == "__main__":
    base_path = os.getcwd()
    #trial to download the video( only audio)
    video_url= "https://www.youtube.com/watch?v=Aty3Wl390Og" 
      
    # Renaming the YT Video--> Audio file to desired name
    video_title = download_youtube_video(video_url, output_path= ".")
    YT_audio_path = r"{}".format(os.path.join(base_path, video_title))
    YT_audio_path_rename= os.path.join(base_path, "audio.mp3")
    if os.path.exists(YT_audio_path_rename):
        # delete the exisitng audio file
        os.remove(YT_audio_path_rename)
    if os.path.exists(YT_audio_path_rename):
        print("the file still exists")
    os.rename(YT_audio_path,YT_audio_path_rename)

    
    """
    # Load Whisper model
    whisper_model = whisper.load_model("large")
    print(whisper)
    #transcription = WhisperTranscription(whisper_model)
    #output = transcription.run(audio_file_path=YT_audio_path_rename)


      
    # Load LLaMA or a similar model for summarization
    summarization_model_name = "facebook/bart-large-cnn"  # Example model; replace with actual LLaMA model if available
    summarization_model = AutoModelForSeq2SeqLM.from_pretrained(summarization_model_name)
    summarization_tokenizer = AutoTokenizer.from_pretrained(summarization_model_name)  


    # Initialize nodes
    transcription_node = WhisperTranscription(whisper_model)
    summarization_node = Summarization(summarization_model, summarization_tokenizer)
    
    # Create the pipeline
    pipeline = Pipeline()
    pipeline.add_node(component=transcription_node, name="WhisperTranscription", inputs=["File"])
    pipeline.add_node(component=summarization_node, name="Summarization", inputs=["WhisperTranscription"])
    
    
    
    # Run the pipeline
    result = pipeline.run(audio_file_path)
    
    # Print the results
    print("Transcription:", result["WhisperTranscription"]["text"])
    print("Summary:", result["Summarization"]["summary"]) 
    """
    # Example audio file path
    audio_file_path = YT_audio_path_rename
    model_name_or_path = "TheBloke/Llama-2-7B-32K-Instruct-GPTQ"
    prompt_model = intialize_model(model_name_or_path)
    prompt_node = initialize_prompt_node(model=prompt_model)

    summary_output = transcribe_audio(file_path= audio_file_path, prompt_node= prompt_node)
    print("Summary", summary_output)