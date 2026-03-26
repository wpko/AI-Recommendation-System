from fastapi import FastAPI
from pydantic import BaseModel
from model.recommender import recommend

app = FastAPI()

class MovieInput(BaseModel):
    title:str
    
@app.get("/")
def home():
    return{"message":"Recommendation API running"}

@app.post("/recommend")
def get_recommendations(data:"MovieInput"):
    movie_title=data.title
    results = recommend(movie_title)
    return {
        "input_movie":movie_title,
        "recommendations":results
    }