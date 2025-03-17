#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import tempfile
from search_engine import audio_to_text, search_subtitles
import os
from pydub import AudioSegment

st.title("🎬 Video Subtitle Search Engine")

uploaded_file = st.file_uploader("Upload a 4-5 min audio clip (MP3 or WAV)", type=["mp3", "wav"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        if uploaded_file.name.endswith(".mp3"):
            audio = AudioSegment.from_mp3(uploaded_file)
            audio.export(temp_audio.name, format="wav")
        else:
            temp_audio.write(uploaded_file.getbuffer())
        
        temp_audio_path = temp_audio.name

    st.write("Processing audio...")
    query_text = audio_to_text(temp_audio_path)
    
    st.subheader("Transcribed Query:")
    st.write(query_text)

    st.write("🔍 Searching subtitles...")
    results = search_subtitles(query_text)

    st.subheader("📜 Top Matching Subtitles:")
    for res in results:
        st.write(f"**{res['text']}** (Subtitle ID: {res['subtitle_id']})")
        st.markdown(f"[View Full Subtitle](https://www.opensubtitles.org/en/subtitles/{res['subtitle_id']})", unsafe_allow_html=True)

