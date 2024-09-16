from haystack import Pipeline
#from haystack.document_stores.in_memory import InMemoryDocumentStore   # only such thing in Haystck which are not components but components can intercat with them
import whisper











if __name__ == "__main__":
    pipeline = Pipeline()

    #document_store = InMemoryDocumentStore()
    model = whisper.load_model("base")
    result = model.transcribe(r"D:/Python_Projects/Video_Summarization_Using_AI/audio.mp3", task = "translate")
    print(result["text"])

