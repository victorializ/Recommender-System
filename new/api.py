import json
import flask
from flask import request
from system import get_recommendations, rate, get_movie, get_highly_rated
from ast import literal_eval

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/recommendations/', methods=['GET'])
def recommendations():
    query_parameters = request.args
    id = query_parameters.get('id')
    recommendations = get_recommendations(int(id))
    return str(recommendations)

@app.route('/recommendations/report', methods=['GET'])
def recommendations_report():
    query_parameters = request.args
    id = query_parameters.get('id')
    top_rated = get_highly_rated(int(id))
    top_rated_info = [get_movie(movie)[['title', 'genres', 'keywords']] for movie in top_rated]
    movies_info = ''
    for i, movie in enumerate(top_rated_info):
        title = movie['title'].values[0]
        genres = literal_eval(movie['genres'].values[0])
        genres = [g['name'] for g in genres]
        genres = ', '.join(genres)
        keywords = literal_eval(movie['keywords'].values[0])
        keywords = [k['name'] for k in keywords]
        keywords = ', '.join(keywords[:5])
        info = f'{i+1}. {title}\n    Genres: {genres}\n    Keywords: {keywords}...'
        movies_info += f'{info}\n'
    recommendations = get_recommendations(int(id))
    recommendations_data = [get_movie(movie)[['title', 'genres', 'keywords']] for movie in recommendations]
    recommendations_info = ''
    for j, movie in enumerate(recommendations_data):
        title = movie['title'].values
        if(len(title)==0):
            continue
        title = title[0]
        genres = literal_eval(movie['genres'].values[0])
        genres = [g['name'] for g in genres]
        genres = ', '.join(genres)
        keywords = literal_eval(movie['keywords'].values[0])
        keywords = [k['name'] for k in keywords]
        keywords = ', '.join(keywords[:5])
        info = f'{j-i}. {title}\n    Genres: {genres}\n    Keywords: {keywords}...'
        recommendations_info += f'{info}\n'
    report = f"User with id: {id} \n\nHighly rated movies:\n{movies_info}\n\nReccomendations:\n{recommendations_info}"
    #return str(get_recommendations(int(id)))
    return report

@app.route('/movies', methods=['GET'])
def movie():
    query_parameters = request.args
    id = query_parameters.get('id')
    movie = get_movie(int(id))
    data = movie.to_json(orient='records', indent=2)
    response = flask.Response(data)
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/rate', methods=['POST'])
def rating():
    data = request.json
    rate(data['userId'], data['movieId'], data['rating'])
    return 'Rated!'

app.run()