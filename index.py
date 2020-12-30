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

#evaluate model
from surprise.model_selection import train_test_split, cross_validate
results = cross_validate(
    algo = algo, data = data, measures=['RMSE'], 
    cv=5, return_train_measures=True
)
    
print(results['test_rmse'].mean())

#CONTENTBASED FILTERING
#preprocess text
df_credits.pop('title')
df_credits.columns = ['id', 'cast', 'crew']
df = df_credits.merge(df_movies, on='id')
#extract first N values of each feature
from ast import literal_eval
features = ['keywords', 'genres', 'cast']
df_copy = pandas.DataFrame()

def head(arr, N = 3):
    #if len(arr) > N:
    #    arr = arr[:N]
    return arr

def clean_value(value):
    return str.lower(value.replace(" ", ""))

def to_string_of_values(arr):
    values = [clean_value(obj['name']) for obj in head(literal_eval(arr))]
    return ' '.join(values)

for feature in features:
    df_copy[feature] = df[feature].copy().apply(to_string_of_values)

#combine features into item profile
def create_metadata_soup(row):
    string = ' '
    for feature in features:
        string += row[feature]
    return string
df_copy['profile'] = df_copy.apply(create_metadata_soup, axis=1)

#create tfidf matrix on item profiles
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocess_text import preprocess_text
vectoriser = TfidfVectorizer(analyzer=preprocess_text)
matrix = vectoriser.fit_transform(df_copy['profile'])

from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(matrix, matrix)

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