import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]

    recommended = []
    recommend_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from API
        recommend_posters.append(fetch_poster(movie_id))
        recommended.append(movies.iloc[i[0]].title)
    return recommended,recommend_posters

movies_dict = pickle.load(open('Movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommendation System")

Selected_movie_name = st.selectbox("Which movies would you like to be recommended?", movies['title'].values)

if st.button("Recommend"):
    recommended,recommend_posters = recommend(Selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended[0])
        st.image(recommend_posters[0])
    with col2:
        st.text(recommended[1])
        st.image(recommend_posters[1])

    with col3:
        st.text(recommended[2])
        st.image(recommend_posters[2])
    with col4:
        st.text(recommended[3])
        st.image(recommend_posters[3])
    with col5:
        st.text(recommended[4])
        st.image(recommend_posters[4])
    #for i in recommendations:
        #st.write(i)

