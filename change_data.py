import pandas as pd

# Tên cột từ file u.item
columns = [
    'movieId', 'title', 'release_date', 'video_release_date', 'IMDb_URL',
    'unknown', 'Action', 'Adventure', 'Animation', "Children's", 'Comedy',
    'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
    'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'
]

movies = pd.read_csv('ml-100k/u.item', sep='|', encoding='latin-1', names=columns)

# Gộp các cột thể loại thành 1 cột "genres"
genre_cols = columns[5:]
movies['genres'] = movies[genre_cols].apply(lambda row: ', '.join([genre for genre, val in zip(genre_cols, row) if val == 1]), axis=1)

# Chỉ giữ lại các cột cần
movies = movies[['movieId', 'title', 'genres']]

# Lưu file
movies.to_csv('data/movies.csv', index=False)
print("✅ Đã tạo movies.csv")

# Tải dữ liệu đánh giá từ file u.data
ratings = pd.read_csv('ml-100k/u.data', sep='\t', names=['userId', 'movieId', 'rating', 'timestamp']) 
# Lưu file CSV
ratings.to_csv('data/ratings.csv', index=False)
print("✅ Đã tạo ratings.csv")  