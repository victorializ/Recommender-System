import pandas
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from preprocess_text import preprocess_text
from keys import Keys

def get_tfidf_matrix(df):
    vectoriser = TfidfVectorizer(analyzer=preprocess_text)
    tfidf_matrix = vectoriser.fit_transform(df)
    return tfidf_matrix
    
def get_item_index(df, value, key):
    indices = pandas.Series(df.index, index=df[key])
    return indices[value]

def get_similarity_rating(tfidf_matrix, index):
    cosine_similarity = linear_kernel(tfidf_matrix, tfidf_matrix)
    similarity_scores = list(enumerate(cosine_similarity[index]))
    return sorted(similarity_scores, key=lambda x: x[1], reverse=True)

def get_recommendations(df, item_id, N, text_key=Keys.text, id_key=Keys.id):
    index = get_item_index(df, item_id, id_key)
    tfidf_matrix = get_tfidf_matrix(df[text_key])

    sorted_similarity_scores = get_similarity_rating(tfidf_matrix, index)

    best_similarity_scores = sorted_similarity_scores[1:N+1]
    most_similar_items_indices = [val[0] for val in best_similarity_scores]
    recommendations = df.iloc[most_similar_items_indices]

    return recommendations