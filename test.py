import whisper
from haystack.translator import Transcriber

# Load a pre-trained whisper model
whisper_model = whisper.load_model("large")

# Initialize the transcriber with the whisper model
transcriber = Transcriber(model=whisper_model)

# Transcribe audio
audio_file_path = "path/to/your/audio.wav"
transcription = transcriber.transcribe(audio_file_path=audio_file_path)

print("Transcription:", transcription)