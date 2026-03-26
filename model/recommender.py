import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process
import numpy as np
#load embeddings
embeddings = np.load("embeddings.npy")

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
    data['Synopsis']+" "+
    data['genre']*3 +" "+
    data['Director']*2 +" "+
    data['Content']
)

data['content'] = data['content'].str.lower()
#6.Index Mapping
indices = pd.Series(data.index,index=data['Title']).drop_duplicates()
#7.Fuzzy Search
def find_closest_title(user_input):
    choices = data['Title'].tolist()
    match, score, _ = process.extractOne(user_input.lower(),choices)
    if score<60:
        return None
    return match

#8.Recommendation Function
def recommend(movie_title,top_n=10):
    closest_title = find_closest_title(movie_title)
    if closest_title is None:
        return ['Movie is not found']
    print(f"Did you mean: {closest_title}")
    idx = indices[closest_title]
    #semantic similarity
    sim_scores = cosine_similarity(
        [embeddings[idx]],
        embeddings,
    ).flatten()
    #filter
    target_genre = data.loc[idx, "genre"].lower()

    sim_scores = [
        (i, s) for i, s in enumerate(sim_scores)
        if s > 0.35 
        and i != idx 
        and any(g in data.loc[i, "genre"].lower() for g in target_genre.split(","))
    ]
    #Sort
    sim_scores = sorted(sim_scores,key=lambda x:x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]
    return data['Title'].iloc[movie_indices].tolist()

