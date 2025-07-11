# downloader/yt_handler.py

from youtubesearchpython import VideosSearch
import yt_dlp
import os
import re

DOWNLOAD_DIR = "downloads"

def search(query, limit=20):
    search = VideosSearch(query, limit=limit)
    return search.result().get("result", [])

def safe_filename(title):
    return re.sub(r'[\\/*?:"<>|]', "", title)

def download_audio(url, output_path=DOWNLOAD_DIR):
    # Step 1: Get metadata
    info_opts = {'quiet': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(info_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        raw_title = info['title']
        channel = info.get('uploader', 'Unknown')
    
    # Format filename
    clean_title = safe_filename(raw_title.split('|')[0].split('-')[0].strip())
    channel = safe_filename(channel.strip())
    filename = f"{clean_title} - {channel}.mp3"
    filename_template = os.path.join(output_path, f"{clean_title} - {channel}.%(ext)s")

    # Step 2: Download
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": filename_template,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    final_path = os.path.join(output_path, filename)
    return final_path, filename
