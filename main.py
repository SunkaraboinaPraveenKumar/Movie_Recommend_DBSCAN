import streamlit as st
import random
import pandas as pd

# Load dataset
df_movies = pd.read_csv("clustered_movies.csv")

# Make sure the movie names are in a column 'movie_name'
df_movies['name'] = df_movies['name'].str.lower()  # Convert movie names to lowercase for consistency


def recommend_movie(movie_name: str, n_recommendations=5):
    movie_name = movie_name.lower()

    # Filter movies based on the input movie name
    movie = df_movies[df_movies['name'].str.contains(movie_name, na=False)]

    if not movie.empty:
        cluster = movie['dbscan_clusters'].values[0]
        cluster_movies = df_movies[df_movies['dbscan_clusters'] == cluster]

        # Select recommended movies
        if len(cluster_movies) >= 5:
            recommended_movies = random.sample(list(cluster_movies['name']), n_recommendations)
        else:
            recommended_movies = list(cluster_movies['name'])
        return recommended_movies
    else:
        return ["Movie not found in the dataset"]


# Streamlit App
st.title("Movies Recommendation System Using DBSCAN Clustering")
st.write("--------------------------------------------------------")
st.subheader("Support Databases")
st.write("1: Netflix TV Shows and Movies")
st.write("2: HBO Max TV Shows and Movies")
st.write("3: Amazon Prime TV Shows and Movies")
st.write("--------------------------------------------------------")

# Populate dropdown with movie names
movie_names = df_movies['name'].unique()
movie_name_input = st.selectbox('Search For a Movie You Like', options=movie_names)

if st.button("Recommend Movies"):
    st.write("### We recommend you these movies:")
    recommendations = recommend_movie(movie_name_input)
    st.dataframe(recommendations)
