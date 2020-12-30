import numpy
import pandas 
import calendar
import time
from ast import literal_eval

df_movies = pandas.read_csv('movies.csv')

def get_recommendations(userId, N=20): 
    df_ratings = pandas.read_csv('ratings_small.csv')
    existing_movies_ids = df_movies['id'].tolist()
    df_ratings = df_ratings[df_ratings['movieId'].isin(existing_movies_ids)]
    user = df_ratings.loc[df_ratings['userId'] == userId]
    rated_ids = user['movieId'].tolist()
    if(len(rated_ids) == 0):
        top = pandas.read_csv('generic_top.csv')
        return list(top['id'].values)[0:N]
    baseline = user['rating'].mean()
    #get list with ids of items with rating more than avarage
    top_ratings = user.loc[user['rating'] > baseline]
    top_rated_ids = top_ratings['movieId'].tolist()

    reccomendations = []
    for val in top_rated_ids:
       movie = df_movies.loc[df_movies['id'] == val] 
       similar = literal_eval(movie['similar'].values[0])
       neigh = literal_eval(movie['neighborhood'].values[0])
       reccomendation = similar + neigh
       reccomendations.extend(reccomendation)

    unique = list(dict.fromkeys(reccomendations))
    not_rated = [val for val in unique if val not in rated_ids]
    #return df_movies[df_movies['id'].isin(not_rated)]
    return not_rated

def rate(userId, movieId, rating):
    gmt = time.gmtime() 
    ts = str(calendar.timegm(gmt))
    df = pandas.DataFrame([[userId, movieId, rating, ts]])
    f = open("ratings_small.csv", "a")
    f.write(df.to_csv(index=False, header=False))
    f.close()

def get_movie(id):
    movie = df_movies.loc[df_movies['id'] == id]
    return movie