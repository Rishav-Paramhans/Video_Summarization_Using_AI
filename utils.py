from pytube import YouTube
import torch
import whisper
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from haystack import Pipeline
from haystack.nodes import BaseComponent



class WhisperTranscription(BaseComponent):
    def __init__(self, model):
        self.model = model
    
    def run(self, audio_file_path):
        result = self.model.transcribe(audio_file_path)
        return {"text": result["text"]}

class Summarization(BaseComponent):
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
    
    def run(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
        summary_ids = self.model.generate(inputs["input_ids"], max_length=150, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return {"summary": summary}




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
        stream = yt.streams.get_highest_resolution()
        
        # Download the video
        print(f"Downloading '{yt.title}'...")
        stream.download(output_path=output_path)
        print(f"Download completed! Video saved to '{output_path}'")
        
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
      
      # trial to download the video
      #video_url= "https://www.youtube.com/watch?v=Aty3Wl390Og" 
      #download_youtube_video(video_url, output_path='.')

      device = 'cuda:' if torch.cuda.is_available() else 'cpu'   
      print(device)   

      # Load Whisper model
      whisper_model = whisper.load_model("base")
      
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
      
      # Example audio file path
      audio_file_path = "path_to_your_audio_file.wav"
      
      # Run the pipeline
      result = pipeline.run(audio_file_path)
      
      # Print the results
      print("Transcription:", result["WhisperTranscription"]["text"])
      print("Summary:", result["Summarization"]["summary"]) 