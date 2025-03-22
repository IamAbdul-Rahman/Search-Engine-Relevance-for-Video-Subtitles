
import streamlit as st
import tempfile
import chromadb
from search_engine import audio_to_text, search_subtitles
import os
from pydub import AudioSegment

st.title("🎥 SubSearch AI")
st.subheader("Subtitle Search Engine Powered by NLP & ML")

uploaded_file = st.file_uploader("Upload a 4-5 min audio clip (MP3 or WAV)", type=["mp3", "wav"])

