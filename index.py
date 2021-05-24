from data.keys import Keys
from data.read import read_data, read_ratings
from data.convert import to_string_of_values
from services.demographic_filtering import general_rate
from services.content_based_filtering import get_recommendations, add_profile

N = 10
data = read_data()
ratings = read_ratings()

#print('Top rated')
#top_rated = general_rate(data).head(N)
#print(top_rated[['title']])

#print('Overview based recommendations')
#overview_based = get_recommendations(data, 'Batman Forever', N, id_key=Keys.title, text_key=Keys.text)
#print(overview_based['title'])

#print('Metadata soup based recommendations')
#data = add_metadata_soup(data, [Keys.director, Keys.cast, Keys.keywords, Keys.genres], convert_data=to_string_of_values)
#metadata_based = get_recommendations(data, 'Batman Forever', N, id_key=Keys.title, text_key=Keys.soup)
#print(metadata_based[['title']])

print('Item profile')
data = add_profile(data, [Keys.director, Keys.cast, Keys.keywords, Keys.genres], convert_data=to_string_of_values)
print(data.head(10)[['id', 'title', 'profile']])

print('Ratings')
def select_user_ratings(ratings, userId):
    return ratings.loc[ratings['userId'] == 1]

user_ratings = select_user_ratings(ratings, 1)
baseline = user_ratings['rating'].mean()
print(baseline)