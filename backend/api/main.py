# backend/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.models import recommend_user_cf, recommend_content, hybrid_recommend

app = FastAPI(title="🎬 Movie Recommendation API")

# Allow frontend access if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Movie Recommendation API"}

@app.get("/recommend/collaborative/{user_id}")
def collaborative(user_id: int):
    return recommend_user_cf(user_id)

@app.get("/recommend/content/{movie_id}")
def content_based(movie_id: int):
    return recommend_content(movie_id)

@app.get("/recommend/hybrid/{user_id}")
def hybrid(user_id: int):
    return hybrid_recommend(user_id)
