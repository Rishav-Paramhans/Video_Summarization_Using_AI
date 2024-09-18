import yt_dlp

def download_audio(url: str, output_path: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,  # Download audio only
        'audioformat': 'mp3',  # Save as mp3
        'outtmpl': output_path,  # Output file path
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=F5VQvf5tx_g"
    output_path = "temp_audio.mp3"
    download_audio(url, output_path)