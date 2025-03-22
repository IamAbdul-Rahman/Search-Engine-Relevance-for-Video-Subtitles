
import streamlit as st
import tempfile
import os


st.title("🎥 SubSearch AI")
st.subheader("Subtitle Search Engine Powered by NLP & ML")

uploaded_file = st.file_uploader("Upload a 4-5 min audio clip (MP3 or WAV)", type=["mp3", "wav"])

