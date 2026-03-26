import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

#1.Load data
data = pd.read_csv('data/dataset.csv')

#2.Clean data
data['Synopsis'] = data['Synopsis'].fillna("")
data['genre'] = data['genre'].fillna("")
data['Director'] = data['Director'].fillna("")
data['Content'] = data['Content'].fillna("")

data['Title'] = data['Title'].str.lower()
#Remove duplicate
data = data.drop_duplicates(subset="Title").reset_index(drop=True)

#3.Combine Features
data['content'] = (
    data['Synopsis']+""+
    data['genre']*3 +""+
    data['Director']*2 +""+
    data['Content']
)

data['content'] = data['content'].str.lower()

# 4. Load model
print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 5. Generate embeddings
print("Generating embeddings...")
embeddings = model.encode(data["content"].tolist(), show_progress_bar=True)

# 6. Save
print("Saving embeddings...")
np.save("embeddings.npy", embeddings)

print("Done ✅")