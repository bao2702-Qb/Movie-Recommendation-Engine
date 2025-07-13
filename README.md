# 🎬 Movie Recommendation Engine

This project is a full-stack movie recommendation system using:
- **Collaborative Filtering**
- **Content-Based Filtering**
- **Hybrid Recommendation**
- **Real-time API (FastAPI)**
- **Frontend (HTML + CSS)**

---

## 📁 Project Structure
```
movie-recommendation-engine/
├── backend/
│   ├── api/
│   │   └── main.py                # FastAPI app
│   └── models.py                 # Recommender algorithms
├── data/
│   ├── movies.csv                # Processed movie data
│   └── ratings.csv               # User rating data
├── notebooks/
│   └── Movie_Recommendation_Algorithms.ipynb  # Jupyter notebook with all models
├── frontend_ui_recommendation.html            # User interface
├── requirements.txt
└── README.md
```

---

## 🚀 Setup Instructions
### ✅ 1. Create virtual environment (optional)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### ✅ 2. Install dependencies
```bash
pip install -r requirements.txt
```

### ✅ 3. Run FastAPI server
```bash
uvicorn app.api.main:app --reload
```
Visit: [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI

### ✅ 4. Open frontend UI
Just open `frontend_ui_recommendation.html` in your browser.

---

## 📊 Recommendation Methods

### 👥 Collaborative Filtering
Recommends movies based on similar users’ preferences using user-user similarity.

### 🧠 Content-Based Filtering
Recommends movies based on movie features like title and genre using TF-IDF and cosine similarity.

### ⚖️ Hybrid Recommendation
Combines collaborative and content-based methods for better accuracy.

---

## 📎 Data Source
- MovieLens 100k Dataset: https://grouplens.org/datasets/movielens/100k/

---