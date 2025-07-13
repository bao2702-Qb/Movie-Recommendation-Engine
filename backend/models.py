# backend/models.py
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load data once for reuse
movies = pd.read_csv("data/movies.csv")
ratings = pd.read_csv("data/ratings.csv")

# ---- Collaborative Filtering ---- #
user_movie_matrix = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
user_sim = cosine_similarity(user_movie_matrix)
user_sim_df = pd.DataFrame(user_sim, index=user_movie_matrix.index, columns=user_movie_matrix.index)

def recommend_user_cf(user_id, top_n=5):
    if user_id not in user_sim_df:
        return []
    similar_users = user_sim_df[user_id].sort_values(ascending=False)[1:top_n+1].index
    top_movies = ratings[ratings['userId'].isin(similar_users)] \
                    .groupby('movieId')['rating'].mean() \
                    .sort_values(ascending=False).head(top_n)
    return movies[movies['movieId'].isin(top_movies.index)][['movieId', 'title']].to_dict(orient='records')

# ---- Content-Based Filtering ---- #
movies['combined'] = movies['title'] + ' ' + movies['genres'].fillna('')
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['combined'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend_content(movie_id, top_n=5):
    try:
        idx = movies[movies['movieId'] == movie_id].index[0]
    except IndexError:
        return []
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]
    return movies.iloc[movie_indices][['movieId', 'title']].to_dict(orient='records')

# ---- Hybrid Recommendation ---- #
def hybrid_recommend(user_id, top_n=10):
    user_based = recommend_user_cf(user_id, top_n=5)
    if not user_based:
        return []
    user_movie_ids = [m['movieId'] for m in user_based]
    hybrid_scores = {}
    for movie_id in user_movie_ids:
        similar_movies = recommend_content(movie_id, top_n=5)
        for m in similar_movies:
            hybrid_scores[m['movieId']] = hybrid_scores.get(m['movieId'], 0) + 1
    sorted_hybrid = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
    movie_ids = [mid for mid, _ in sorted_hybrid[:top_n]]
    return movies[movies['movieId'].isin(movie_ids)][['movieId', 'title']].to_dict(orient='records')
