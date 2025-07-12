from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from app.api.recommender import (
    get_user_based_recommendations,
    get_item_based_recommendations,
    get_content_based_recommendations,
    get_hybrid_recommendations,
    search_movies
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/recommend/user/{user_id}")
def recommend_user(user_id: int, k: int = 10):
    return get_user_based_recommendations(user_id, k)

@app.get("/recommend/movie/{movie_id}")
def recommend_movie(movie_id: int, k: int = 10):
    return get_item_based_recommendations(movie_id, k)

@app.get("/recommend/content/{movie_id}")
def recommend_content(movie_id: int, k: int = 10):
    return get_content_based_recommendations(movie_id, k)

@app.get("/recommend/hybrid/{user_id}")
def recommend_hybrid(user_id: int, k: int = 10):
    return get_hybrid_recommendations(user_id, k)

@app.get("/search")
def search(query: str, k: int = 10):
    return search_movies(query, k)

@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})