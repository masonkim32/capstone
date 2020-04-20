# FLASK_APP=api.py FLASK_ENV=development flask run

import datetime
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .auth import AuthError, requires_auth
from .models import setup_db, Movie, Actor


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    return app


app = create_app()


def format_datetime(value):
    date = dateutil.parser.parse(value)
    date_format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, date_format)


app.jinja_env.filters['datetime'] = format_datetime


@app.route('/movies', methods=['GET'])
def retrieve_movies():
    movies = Movie.query.all()
    if len(movies) == 0:
        abort(404)

    movies = [movie.format() for movie in movies]
    return jsonify({
        'success': True,
        'movies': movies
    }), 200


@app.route('/movie/<int:movie_id>', methods=['GET'])
@requires_auth('get:movie')
def retrieve_a_movie(payload, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)

    return jsonify({
        'success': True,
        'movie': movie.format()
    }), 200


@app.route('/movie', methods=['POST'])
@requires_auth('post:movie')
def add_movies(payload):
    try:
        body = request.get_json()

        new_movie = Movie(
            title=body.get('title'),
            release_date=body.get('release_date', None)
        )
        new_movie.insert()

        all_movies = Movie.query.all()

        return jsonify({
            'success': True,
            'created': new_movie.id,
            'total_movies': len(all_movies),
        }), 200
    except Exception:
        abort(422)


@app.route('/movie/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movie')
def delete_movie(payload, movie_id):
    try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        movie.delete()
        all_movies = Movie.query.all()

        if len(all_movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'deleted': movie_id,
            'total_movies': len(all_movies),
        }), 200

    except Exception:
        abort(422)


@app.route('/movie/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movie')
def update_movie(payload, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)

    body = request.get_json()

    movie_title = body.get('title', None)
    if movie_title is not None:
        movie.title = movie_title
    movie_release_date = body.get('release_date', None)
    if movie_release_date is not None:
        movie.release_date = movie_release_date

    try:
        movie.update()
    except Exception as e:
        abort(422)

    return jsonify({
        'success': True,
        'movie': movie.format()
    }), 200


@app.route('/actors', methods=['GET'])
def retrieve_actors():
    actors = Actor.query.all()
    if len(actors) == 0:
        abort(404)

    actors = [actor.format() for actor in actors]
    return jsonify({
        'success': True,
        'actors': actors
    }), 200


@app.route('/actor/<int:actor_id>', methods=['GET'])
@requires_auth('get:actor')
def retrieve_an_actor(payload, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)

    return jsonify({
        'success': True,
        'actor': actor.format()
    }), 200


@app.route('/actor', methods=['POST'])
@requires_auth('post:actor')
def add_actor(payload):
    try:
        body = request.get_json()

        new_actor = Actor(
            name=body.get('name'),
            age=body.get('age'),
            gender=body.get('gender')
        )
        new_actor.insert()

        all_actor = Actor.query.all()

        return jsonify({
            'success': True,
            'created': new_actor.id,
            'total_actors': len(all_actor),
        }), 200
    except Exception:
        abort(422)


@app.route('/actor/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_actor(payload, actor_id):
    try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        actor.delete()
        all_actors = Actor.query.all()

        if len(all_actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'deleted': actor_id,
            'total_movies': len(all_actors),
        }), 200

    except Exception:
        abort(422)


@app.route('/actor/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actor')
def update_actor(payload, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)

    body = request.get_json()

    actor_name = body.get('name', None)
    if actor_name is not None:
        actor.name = actor_name
    actor_age = body.get('age', None)
    if actor_age is not None:
        actor.age = actor_age
    actor_gender = body.get('gender', None)
    if actor_gender is not None:
        actor.gender = actor_gender

    try:
        actor.update()
    except Exception as e:
        abort(422)

    return jsonify({
        'success': True,
        'actor': actor.format()
    }), 200


#####################################################################
# Error Handlers
#####################################################################

@app.errorhandler(400)
def bad_request(error):
    """Error handling for bad request"""
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(401)
def not_authorized(error):
    """Error handling for unauthorized request"""
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Not authorized"
    }), 401


@app.errorhandler(404)
def not_found(error):
    """Error handling for no resources"""

    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    """Error handling for unprocessable entity"""

    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(AuthError)
def process_AuthError(error):
    """Error handler should conform to general task above"""
    response = jsonify(error.error)
    response.status_code = error.status_code

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
