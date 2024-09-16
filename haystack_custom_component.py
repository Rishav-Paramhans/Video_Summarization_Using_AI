from haystack import component, Pipeline
import whisper

# Define the WhisperTranslator component
@component
class WhisperTranlator:
    """
    A component to translate as well as transcribe the audio data
    """
    def __init__(self, input_audio_path: str):
        self.input_audio_path = input_audio_path

    @component.output_types(translated_text=dict)
    def run(self):
        # Load the Whisper model
        model = whisper.load_model("base")
        
        # Transcribe and translate the audio file
        result = model.transcribe(self.input_audio_path, task="translate")
        
        # Return the translated text
        return result


if __name__ == "__main__":
    # Create the pipeline
    pipeline = Pipeline()

    # Input audio file path
    input_audio_path = r"D:/Python_Projects/Video_Summarization_Using_AI/audio.mp3"
    
    # Add the WhisperTranslator component to the pipeline
    whisper_translator = WhisperTranlator(input_audio_path)
    pipeline.add_component(name="whisper_translator", instance= whisper_translator)
    
    # Run the pipeline
    result = pipeline.run({})
    print(result["whisper_translator"]["text"])