import streamlit as st
import pandas as pd
import pickle as pkl
import requests as req
from dotenv import load_dotenv
import os
load_dotenv()
def fetchMoviePoster(moviename):
    try:
        # Make the API request and get the JSON response
        api_key = os.getenv('OMDB_API_KEY')
        data = req.get('https://www.omdbapi.com/?t={}&apikey=7b1365f1#'.format(moviename)).json()

        # Check if the 'Poster' key exists in the response
        if 'Poster' in data and data['Poster'] != 'N/A':
            return data['Poster']
        else:
            return "Poster not available"

    except req.exceptions.RequestException as e:
        # Handle request-related errors (e.g., network issues)
        print(f"Error fetching movie poster: {e}")
        return "Error fetching poster"

    except KeyError:
        # Handle cases where the expected key is not in the JSON response
        print(f"Poster key not found for movie: {moviename}")
        return "Poster not available"



with open('similarity.pkl', 'rb') as file:
    similarity = pkl.load(file)
with open('movies.pkl', 'rb') as file: 
   movie_dict  = pkl.load(file)

movies = pd.DataFrame(movie_dict)
st.title('Movie Recommender System')

def recommend_movie(movie):
    movie_index =movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x : x[1])[1:10]   # first 5 excluding the one whcih is itself
    recommended_movies =[]
    recommended_movies_posters =[]

    for i in movies_list:
        name  =movies.iloc[i[0]].title
        print(name)
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetchMoviePoster(name))
    return recommended_movies, recommended_movies_posters

movieName = st.selectbox(
'enter movie name',
movies['title'].values,
)


if st.button('recomend'):
    recommendations, posters = recommend_movie(movieName)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header(recommendations[0])
        st.image(posters[0])

        st.header(recommendations[3])
        st.image(posters[3])

    with col2:
        st.header(recommendations[1])
        st.image(posters[1])

        st.header(recommendations[4])
        st.image(posters[4])

    with col3:
        st.header(recommendations[2])
        st.image(posters[2])

        st.header(recommendations[5])
        st.image(posters[5])

    col4, col5, col6 = st.columns(3)

    with col4:
        st.header(recommendations[6])
        st.image(posters[6])

    with col5:
        st.header(recommendations[7])
        st.image(posters[7])

    with col6:
        st.header(recommendations[8])
        st.image(posters[8])
   