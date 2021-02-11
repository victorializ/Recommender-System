import pandas

from data.keys import Keys
from data.convert import find_director
from ast import literal_eval

def read_data():
    df_credits = pandas.read_csv('tmdb_5000_credits.csv')
    df_movies = pandas.read_csv('tmdb_5000_movies.csv')
    df_credits.pop(Keys.title)
    df_credits.columns = [Keys.id, Keys.cast, Keys.crew]
    df = df_credits.merge(df_movies, on=Keys.id)
    df[Keys.text] = df[Keys.text].fillna('')
    df[Keys.director] = df[Keys.crew].copy().apply(literal_eval).apply(find_director)
    return df

def read_ratings():
    df = pandas.read_csv('ratings_small.csv')
    return df