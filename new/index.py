import pandas 

#READ DATA
df_credits = pandas.read_csv('tmdb_5000_credits.csv')
df_movies = pandas.read_csv('tmdb_5000_movies.csv')
df_ratings = pandas.read_csv('ratings_small.csv')
#select only ratings of existing movies
existing_movies_ids = df_movies['id'].tolist()
df_ratings = df_ratings[df_ratings['movieId'].isin(existing_movies_ids)]

#GENERALIZED RECCOMENDATIONS to every user, based on item popularity

data = df_movies
C = data['vote_average'].mean() #mean vote across the whole report
m = data['vote_count'].quantile(0.9) #minimum votes required to be listed in the chart
q_items = data.copy().loc[data['vote_count'] >= m] #items with required votes number
def weighted_rating(item):
    v = item['vote_count']
    R = item['vote_average']
    # Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * C)
q_items['scope'] = q_items.apply(weighted_rating, axis=1)
q_items = q_items.sort_values('scope', ascending=False)
f = open("generic_top.csv", "w")
f.write(q_items.to_csv(index=False))
f.close()

#COLLABORATIVE FILTERING
#rename for training model
df = df_ratings.rename(columns={'userId': 'user', 'movieId': 'item'})

from surprise import Dataset
from surprise import Reader
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[["user", "item", "rating"]], reader)
from surprise import KNNWithMeans
sim_options = {
    "name": "pearson",
    "user_based": False
}
algo = KNNWithMeans(sim_options=sim_options)
trainset = data.build_full_trainset()
trainset_iids = list(trainset.all_items())
iid_converter = lambda x: trainset.to_raw_iid(x)
trainset_raw_iids = list(map(iid_converter, trainset_iids))
algo.fit(trainset)
def get_neighbors(itemId, N=5):
    if itemId not in trainset_raw_iids:
        return []
    iid = trainset_raw_iids.index(itemId)
    neighbors_iids = algo.get_neighbors(iid, N)
    ids = list(map(lambda value: trainset_raw_iids[value], neighbors_iids))
    return ids
df_movies['neighborhood'] = df_movies['id'].copy().apply(get_neighbors)

#CONTENTBASED FILTERING
#preprocess text
df_credits.pop('title')
df_credits.columns = ['id', 'cast', 'crew']
df = df_credits.merge(df_movies, on='id')
#extract first N values of each feature
from ast import literal_eval
features = ['keywords', 'genres', 'cast']

import re
charRe = re.compile(r'[^a-zA-Z0-9.]')

def clean_value(value):
    without_spaces = value.replace(" ", "")
    string = charRe.search(without_spaces)
    if not bool(string):
        return str.lower(without_spaces)
    else:
        return ""

def to_string_of_values(arr):
    values = [clean_value(obj['name']) for obj in literal_eval(arr)]
    return ' '.join(values)

for feature in features:
    key = f'{feature}_vector'
    df[key] = df[feature].copy().apply(to_string_of_values)

ids = df['id'].to_list()

from sklearn.feature_extraction.text import CountVectorizer

def vectorize(feature_name):
    feature = df[feature_name].to_list()
    vectorizer = CountVectorizer()
    vector = vectorizer.fit_transform(feature)
    return vectorizer, vector

genres_vectorizer, genres_vector = vectorize('genres_vector')
keywords_vectorizer, keywords_vector = vectorize('keywords_vector')
cast_vectorizer, cast_vector = vectorize('cast_vector')

from sklearn.metrics.pairwise import cosine_similarity
genres_similarity = cosine_similarity(genres_vector, genres_vector)
keywords_similarity = cosine_similarity(keywords_vector, keywords_vector)
cast_similarity = cosine_similarity(cast_vector, cast_vector)

similarity = genres_similarity + keywords_similarity + cast_similarity

def get_similar(id, N=5):
    indices = pandas.Series(df.index, index=df['id'])
    similarity_scores = list(enumerate(similarity[indices[id]]))
    sorted_similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    best_similarity_scores = sorted_similarity_scores[1:N+1]
    most_similar_items_indices = [val[0] for val in best_similarity_scores]
    return most_similar_items_indices

df_movies['similar'] = df_movies['id'].copy().apply(get_similar)

f = open("movies.csv", "w")
f.write(df_movies.to_csv(index=False))
f.close()