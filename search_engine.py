#!/usr/bin/env python
# coding: utf-8

# In[1]:


import chromadb
import json
import wave
import os
from vosk import Model, KaldiRecognizer
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDINGS_DB = "chroma_subtitles"
VOSK_MODEL_PATH = r"C:\Users\hp\Desktop\Innomatics\Task 8\vosk-model-small-en-us-0.15"

def audio_to_text(audio_path):
    """Convert user audio query to text using Vosk."""
    model = Model(VOSK_MODEL_PATH)
    
    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    
    text_result = []
    
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text_result.append(result.get("text", ""))
    
    wf.close()
    return " ".join(text_result)

def search_subtitles(query):
    """Retrieve most relevant subtitles using cosine similarity."""
    client = chromadb.PersistentClient(path=EMBEDDINGS_DB)
    collection = client.get_collection(name="subtitles")

    model = SentenceTransformer(MODEL_NAME)
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=5
    )

    return results["metadatas"][0]

if __name__ == "__main__":
    audio_path = "C:/Users/hp/Desktop/Innomatics/Task 8/aaa.wav"
    query_text = audio_to_text(audio_path)
    results = search_subtitles(query_text)
    
    print("\nTop Matching Subtitles:")
    for res in results:
        print(f"- {res['text']} (Subtitle ID: {res['subtitle_id']})")


# In[ ]:




