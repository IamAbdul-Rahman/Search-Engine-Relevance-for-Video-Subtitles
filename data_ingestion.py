#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import pandas as pd
import zlib
import io
import zipfile

DB_PATH = "C:/Users/hp/Desktop/Innomatics/Task 8/eng_subtitles_database.db"

count = 0

def extract_subtitles(sample_size=30000):
    """Extract and decompress subtitles from the database."""
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT num, name, content FROM zipfiles ORDER BY RANDOM() LIMIT {sample_size};"
    df = pd.read_sql(query, conn)
    conn.close()
    
    

    def decompress(binary_data):
        global count
    # Decompress the binary data using the zipfile module
    # print(count, end=" ")
        count += 1
        with io.BytesIO(binary_data) as f:
            with zipfile.ZipFile(f, 'r') as zip_file:
            # Assuming there's only one file in the ZIP archive
                subtitle_content = zip_file.read(zip_file.namelist()[0])

    # Now 'subtitle_content' should contain the extracted subtitle content
        return subtitle_content.decode('latin-1')  # Assuming the content is UTF-8 encoded text

    df['content'] = df['content'].apply(decompress)
    df.dropna(inplace=True)  # Remove failed decompressions
    return df

if __name__ == "__main__":
    subtitles_df = extract_subtitles()
    subtitles_df.to_csv("subtitles.csv", index=False)
    print("Extracted and saved subtitles to subtitles.csv")


# In[ ]:




