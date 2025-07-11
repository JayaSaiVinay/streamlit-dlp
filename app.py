# app.py

import streamlit as st
import os
from downloader.yt_handler import search, download_audio, safe_filename

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Page settings
st.set_page_config(
    page_title="🎵 DadTunes",
    page_icon="🎶",
    layout="wide"
)

st.markdown(
    """
    <h1 style='text-align: center; font-size: 2.5em;'>🎶 DadTunes</h1>
    <p style='text-align: center;'>Search YouTube and download songs in MP3 format</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# Input box
query = st.text_input("🔍 Search for a song or artist", placeholder="e.g., Arijit Singh Tum Hi Ho")

if query:
    with st.spinner("Searching YouTube..."):
        results = search(query)

    if results:
        st.subheader("🎬 Search Results")
        for i, video in enumerate(results):
            title = video['title']
            thumbnail = video['thumbnails'][0]['url']
            duration = video.get('duration', 'N/A')
            channel = video['channel']['name']
            url = f"https://www.youtube.com/watch?v={video['id']}"

            # Sanitize filename
            clean_title = safe_filename(title)
            file_name = f"{clean_title}.mp3"
            file_path = os.path.join(DOWNLOAD_DIR, file_name)

            with st.container():
                st.markdown("---")
                cols = st.columns([1, 3])
                with cols[0]:
                    st.image(thumbnail, width=140)
                with cols[1]:
                    st.markdown(f"### {title}")
                    st.caption(f"🕒 {duration} &nbsp;&nbsp;&nbsp; 👤 {channel}")

                    if not os.path.exists(file_path):
                        if st.button("🎧 Download Audio", key=f"btn_{i}"):
                            with st.spinner("Downloading audio..."):
                                try:
                                    file_path, file_name = download_audio(url)
                                    st.success("✅ Download complete!")
                                    st.audio(file_path)
                                    with open(file_path, "rb") as f:
                                        st.success("📥 Tap below to save to your phone")
                                        st.download_button("📥 Save MP3", f, file_name)
                                except Exception as e:
                                    st.error(f"❌ Error: {str(e)}")
                    else:
                        st.success("✅ Already downloaded")
                        st.audio(file_path)
                        with open(file_path, "rb") as f:
                            st.download_button("📥 Save MP3", f, file_name)
    else:
        st.warning("No results found. Try a different search.")
