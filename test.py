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
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
from llama_cpp import Llama



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
        # Load the model and tokenizer directly from Hugging Face
        llm = Llama.from_pretrained(
	        repo_id="TheBloke/Llama-2-7B-32K-Instruct-GGUF",
	        filename="llama-2-7b-32k-instruct.Q5_K_S.gguf",
            )


        # Define the input
        input_text = "Summarize the input text in 10 words: {}".format(translated_text.get("text", ""))

        # Print the translated_text to verify its content
        print("Translated Text:", translated_text)
        # Generate a response from the model
        response = llm(prompt=input_text, max_length=200)

        # Extract and return the summary from the response
        summary = response['choices'][0].get('text', 'No summary available.')

        print(response)
        #print("output type", type(summary))
        return {"summary": summary}
    

if __name__ == "__main__":
    # Create the pipeline
    pipeline = Pipeline()

    # Input audio file path
    input_video_url = "https://www.youtube.com/watch?v=vJNjaaylllY"
    
 
    summarizer = Summarizer()


    pipeline.draw(path=r"./local_path.png")
    # Run the pipeline
    input_text= {"text": "One way forward here could be to add a debug arg to Pipeline.run() and every node.run(). If True the node can write information to the _debug key introduced in #1321 .Ideally, we are not only returning this debug information at the very end but already print/log it along the way."}
    result = pipeline.run(input_text)
    print("Final pipeline result:", result)

    # Access the summary explicitly if not already in the result
    if 'Summarizer' in result:
        print("Summary:", result['Summarizer'])
    else:
        print("Summarizer output missing.")