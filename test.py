from youtube_transcript_api import YouTubeTranscriptApi

youtube_vid_url = "https://www.youtube.com/watch?v=-a6E-r8W2Bs"

video_id = youtube_vid_url.split("=")[1]
transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
print(transcript_text)