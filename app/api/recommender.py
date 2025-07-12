from fastapi import HTTPException
import pandas as pd
import pickle

movies = pd.read_csv("data/movies.csv")
ratings = pd.read_csv("data/ratings.csv")

with open("app/models/user_similarity.pkl", "rb") as f:
    user_similarity = pickle.load(f)
with open("app/models/movie_similarity.pkl", "rb") as f:
    movie_similarity = pickle.load(f)
with open("app/models/content_similarity.pkl", "rb") as f:
    content_similarity = pickle.load(f)

user_movie_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
movie_ids = user_movie_matrix.columns
user_ids = user_movie_matrix.index

def get_user_based_recommendations(user_id: int, k: int = 10):
    if user_id not in user_ids:
        raise HTTPException(status_code=404, detail="User ID not found")
    sim_scores = list(enumerate(user_similarity[user_id - 1]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_users = [idx + 1 for idx, _ in sim_scores[1:11]]
    movie_scores = user_movie_matrix.loc[sim_users].mean().sort_values(ascending=False)
    seen_movies = user_movie_matrix.loc[user_id][user_movie_matrix.loc[user_id] > 0].index
    recommended = movie_scores.drop(seen_movies).head(k)
    return movies[movies["movieId"].isin(recommended.index)][["movieId", "title"]].to_dict(orient="records")

def get_item_based_recommendations(movie_id: int, k: int = 10):
    if movie_id not in movie_ids:
        raise HTTPException(status_code=404, detail="Movie ID not found")
    sim_scores = list(enumerate(movie_similarity[movie_ids.get_loc(movie_id)]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    similar_movies = [movie_ids[idx] for idx, _ in sim_scores[1:k+1]]
    return movies[movies["movieId"].isin(similar_movies)][["movieId", "title"]].to_dict(orient="records")

def get_content_based_recommendations(movie_id: int, k: int = 10):
    if movie_id not in movie_ids:
        raise HTTPException(status_code=404, detail="Movie ID not found")
    sim_scores = list(enumerate(content_similarity[movie_ids.get_loc(movie_id)]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    similar_movies = [movie_ids[idx] for idx, _ in sim_scores[1:k+1]]
    return movies[movies["movieId"].isin(similar_movies)][["movieId", "title"]].to_dict(orient="records")

def get_hybrid_recommendations(user_id: int, k: int = 10):
    user_recs = get_user_based_recommendations(user_id, k * 2)
    hybrid_scores = {}
    for rec in user_recs:
        movie_id = rec["movieId"]
        content_recs = get_content_based_recommendations(movie_id, k=5)
        for m in content_recs:
            mid = m["movieId"]
            hybrid_scores[mid] = hybrid_scores.get(mid, 0) + 1
    sorted_movies = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
    top_ids = [mid for mid, _ in sorted_movies[:k]]
    return movies[movies["movieId"].isin(top_ids)][["movieId", "title"]].to_dict(orient="records")

def search_movies(query: str, k: int = 10):
    result = movies[movies["title"].str.contains(query, case=False, na=False)]
    return result[["movieId", "title"]].head(k).to_dict(orient="records")