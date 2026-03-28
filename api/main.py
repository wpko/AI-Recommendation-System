from fastapi import FastAPI
from pydantic import BaseModel
from model.recommender import recommend
from model.recommender import data
import requests

API_KEY = "a9c2b4ee901a79f30f9e5afb84a996eb"

app = FastAPI()

class MovieInput(BaseModel):
    title:str
    
def get_poster(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"
    res = requests.get(url).json()
    
    if res['results']:
        poster_path = res['results'][0]['poster_path']
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None
    
@app.get("/search")
def search_movies(query:str):
    results=[
        title for title in data['Title']
        if query.lower() in title.lower()
    ]
    return results[:10]
    
@app.get("/")
def home():
    return{"message":"Recommendation API running"}

@app.post("/recommend")
def get_recommendations(data_input: MovieInput):
    movie_title=data_input.title
    results = recommend(movie_title,top_n=10)
    #addposter
    enriched = []
    for item in results:
        poster = get_poster(item['title'])
        enriched.append({
            'title': item['title'],
            'score': item['score'],
            'poster': poster
        })
    return {
        "input_movie": movie_title,
        "recommendations": enriched
    }