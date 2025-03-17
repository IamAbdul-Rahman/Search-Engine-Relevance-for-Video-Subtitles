#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDINGS_DB = "chroma_subtitles"
BATCH_SIZE = 100

def chunk_text(text, max_length=500, overlap=50):
    """Chunk long subtitle content into overlapping segments."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_length - overlap):
        chunk = " ".join(words[i:i + max_length])
        chunks.append(chunk)
    return chunks

def create_embeddings():
    """Generate embeddings for subtitle chunks and store in ChromaDB."""
    client = chromadb.PersistentClient(path=EMBEDDINGS_DB)
    collection = client.get_or_create_collection(name="subtitles")

    df = pd.read_csv("subtitles.csv")
    model = SentenceTransformer(MODEL_NAME)

    for index, row in df.iterrows():
        chunks = chunk_text(row['content'])
        embeddings = model.encode(chunks, batch_size=BATCH_SIZE).tolist()
        
        for idx, emb in enumerate(embeddings):
            collection.add(
                ids=[f"{row['num']}_{idx}"], 
                embeddings=[emb], 
                metadatas=[{"subtitle_id": row['num'], "text": chunks[idx]}]
            )
    
    print("Subtitle embeddings stored in ChromaDB.")

if __name__ == "__main__":
    create_embeddings()

