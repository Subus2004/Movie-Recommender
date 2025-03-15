import pickle
import streamlit as st
import requests
from PIL import Image
import time

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path', '')
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
        return full_path
    except Exception as e:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    
    return recommended_movie_names, recommended_movie_posters

# Set page layout
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Custom Background
st.markdown("""
    <style>
        .main {background-color: #0d1117 !important; color: white !important;}
        h1 {color: #ffcc00; text-align: center;}
        .stButton>button {background-color: #ffcc00; color: black; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

# Load Data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Type or select a movie from the dropdown", movie_list)

if st.button('🔍 Show Recommendations'):
    with st.spinner("Finding the best matches for you..."):
        time.sleep(2)  # Simulating loading time
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    st.subheader("Recommended Movies 🎥")
    
    cols = st.columns(5)  # Create 5 columns dynamically
    for i in range(5):
        with cols[i]:
            st.image(recommended_movie_posters[i], use_container_width=True)
            st.markdown(f"**{recommended_movie_names[i]}**")

# Footer
st.markdown("""
    <hr>
    <p style='text-align:center;'>Made with ❤️ by Movie Enthusiasts | Powered by TMDB API</p>
""", unsafe_allow_html=True)
    