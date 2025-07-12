from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import pickle
import os

def generate_similarity_matrices():
    print("Loading data...")
    movies = pd.read_csv("data/movies.csv")
    ratings = pd.read_csv("data/ratings.csv")

    # User-Movie Matrix
    matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)

    # User Similarity
    print("Computing user similarity...")
    user_similarity = cosine_similarity(matrix)
    with open("app/models/user_similarity.pkl", "wb") as f:
        pickle.dump(user_similarity, f)

    # Item Similarity
    print("Computing movie similarity...")
    movie_similarity = cosine_similarity(matrix.T)
    with open("app/models/movie_similarity.pkl", "wb") as f:
        pickle.dump(movie_similarity, f)

    # Content Similarity
    print("Computing content similarity...")
    movies["combined"] = movies["genres"].fillna("") + " " + movies["title"].fillna("")
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies["combined"])
    content_similarity = cosine_similarity(tfidf_matrix)
    with open("app/models/content_similarity.pkl", "wb") as f:
        pickle.dump(content_similarity, f)

    print("All .pkl files generated successfully.")