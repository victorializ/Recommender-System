import flask
from flask import request
from system import get_recommendations, rate, get_movie

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/recommendations', methods=['GET'])
def recommendations():
    query_parameters = request.args
    id = query_parameters.get('id')
    return str(get_recommendations(int(id)))

@app.route('/movies', methods=['GET'])
def movie():
    query_parameters = request.args
    id = query_parameters.get('id')
    return get_movie(int(id)).to_json(orient='records', indent=2)

@app.route('/rate', methods=['POST'])
def rating():
    data = request.json
    rate(data['userId'], data['movieId'], data['rating'])
    return 'Rated!'

app.run()