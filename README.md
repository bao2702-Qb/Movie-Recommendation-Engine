"""
# Movie Recommendation System

This project is a personalized movie recommender system based on collaborative filtering, content-based filtering, and a hybrid approach, served through a FastAPI interface.

## Features
- User-Based Collaborative Filtering
- Item-Based Collaborative Filtering
- Content-Based Filtering (genres, titles)
- Hybrid Filtering
- Real-time API

## Setup
```bash
pip install -r requirements.txt
uvicorn app.api.main:app --reload
```

## API Endpoints
- `/recommend/user/{user_id}`
- `/recommend/movie/{movie_id}`
- `/recommend/content/{movie_id}`
- `/recommend/hybrid/{user_id}`
"""