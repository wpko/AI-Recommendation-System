import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process
import numpy as np

import os
#load embeddings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(BASE_DIR, "..", "data", "dataset.csv")
embedding_path = os.path.join(BASE_DIR, "..", "embeddings.npy")

data = pd.read_csv(data_path)
embeddings = np.load(embedding_path)

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

def is_scifi(genre):
    genre = genre.lower()
    return (
        "sci-fi" in genre or
        "science-fiction" in genre or
        "science fiction" in genre
    )

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
    sim_scores = sim_scores = [
        (i, s) for i, s in enumerate(sim_scores)
        if s > 0.3   # 🔥 reduce threshold
        and i != idx
        and is_scifi(data.loc[i, "genre"])
        and "fantasy" not in data.loc[i,"genre"].lower()
    ]
    if len(sim_scores) == 0:
        sim_scores = [
            (i,s) for i, s in enumerate(sim_scores)
            if s>0.25 and i!=idx 
        ]
    #Sort
    sim_scores = sorted(sim_scores,key=lambda x:x[1], reverse=True)
    sim_scores = sim_scores[:min(top_n, len(sim_scores))]
    
    #return title + score
    return[
        {
            'title': data['Title'].iloc[i],
            'score': round(float(s),2)
        }
        for i, s in sim_scores
    ]

