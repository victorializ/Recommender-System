import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics.pairwise import linear_kernel

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from services.preprocess_text import preprocess_text
from data.keys import Keys

def tfidf_vectorise(df):
    vectoriser = TfidfVectorizer(analyzer=preprocess_text)
    matrix = vectoriser.fit_transform(df)
    return matrix

def count_vectorise(df):
    vectoriser = CountVectorizer(analyzer=preprocess_text)
    matrix = vectoriser.fit_transform(df)
    return matrix
    
def get_item_index(df, value, key):
    indices = pandas.Series(df.index, index=df[key])
    return indices[value]

def get_similarity_rating(matrix, index):
    similarity = cosine_similarity(matrix, matrix)
    similarity_scores = list(enumerate(similarity[index]))
    return sorted(similarity_scores, key=lambda x: x[1], reverse=True)

def get_recommendations(df, item_id, N, text_key=Keys.text, id_key=Keys.id, vectorise=tfidf_vectorise):
    index = get_item_index(df, item_id, id_key)
    matrix = vectorise(df[text_key])

    sorted_similarity_scores = get_similarity_rating(matrix, index)

    best_similarity_scores = sorted_similarity_scores[1:N+1]
    most_similar_items_indices = [val[0] for val in best_similarity_scores]
    recommendations = df.iloc[most_similar_items_indices]

    return recommendations

def create_metadata_soup(features):
    def create(row):
        string = ' '
        for feature in features:
            string += row[feature]
        return string   
    return create 

def add_profile(df, features, convert_data):
    df_copy = pandas.DataFrame()

    for feature in features:
        df_copy[feature] = df[feature].copy().apply(convert_data)

    metadata_soup = create_metadata_soup(features)
    df_copy[Keys.profile] = df_copy.apply(metadata_soup, axis=1)
    matrix = tfidf_vectorise(df_copy[Keys.profile])
    print(df.size)
    print(matrix.size)
    df[Keys.profile] = matrix
    return df