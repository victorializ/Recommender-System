import pandas

from keys import Keys
from services.demographic_filtering import general_rate
from services.content_based_filtering import get_recommendations

from add_soup import add_soup

def read_data():
    df_credits = pandas.read_csv('tmdb_5000_credits.csv')
    df_movies = pandas.read_csv('tmdb_5000_movies.csv')
    df_credits.pop(Keys.title)
    df_credits.columns = [Keys.id, Keys.cast, Keys.crew]
    df = df_credits.merge(df_movies, on=Keys.id)
    df[Keys.text] = df[Keys.text].fillna('')
    return df

data = read_data()

print('Top rated')
top_rated = general_rate(data).head(10)
print(top_rated[['title']])

print('Overview based recommendations')
overview_based = get_recommendations(data, 'Batman Forever', 10, id_key=Keys.title, text_key=Keys.text)
print(overview_based['title'])

print('Soup based recommendations')
data = add_soup(data, [Keys.cast, Keys.keywords, Keys.genres])
soup_based = get_recommendations(data, 'Batman Forever', 10, id_key=Keys.title, text_key=Keys.soup)
print(soup_based[['title']])