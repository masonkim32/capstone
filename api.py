"""api.py

This is the main module of the Flask app: 'Casting Agency'.
This app provide the functionality for creating movies and managing
and assigning actors to those movies.

- Author: Mason Kim (icegom@gmail.com)
- Start code is provided by Udacity

Example:
    FLASK_APP=api.py FLASK_ENV=development flask run
"""
import datetime
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .auth.auth import AuthError, requires_auth
from .database.models import setup_db, Movie, Actor


#####################################################################
# Initial setups
#####################################################################

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



######################################################################
# Endpoint functions
######################################################################

@app.route('/movies', methods=['GET'])
def retrieve_movies():
    """An endpoint to handle GET requests '/movies'

    Retrieve a list of all movies from database

    Return:
        Status code 200 and json object with
            "success": True or False
            "movies": the list of movies
    Raises:
        404: Resource is not found if any movie is not existed.
    """
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
    """An endpoint to handle GET requests '/movie/<int:movie_id>'

    Retrieve the movie data with provided id from database

    Arguments:
        payload (dict): decoded jwt payload
        movie_id (int): movie id which is wanted to retrieve
    Return:
        Status code 200 and json object with
            "success": True or False
            "movie": json object of movie data
    Raises:
        404: Resource is not found if the movie with provided id is
            not existed.
    """
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
    """An endpoint to handle POST request '/movie'

    Add a new movie in the movies table when the request user have
    a proper permission.

    Arguments:
        payload (dict): decoded jwt payload
    Returns:
        Status code 200 and json object with
            "success": True or False
            "created": The id of newly creacted movie data
            "total_movies": The number of movies after adding
                            the new movie
    Raises:
        400: Title or release_date has not been submitted.
        422: Request is unprocessable.
    """
    try:
        body = request.get_json()
        title=body.get('title'),
        release_date=body.get('release_date', None)
        if not title or not release_date:
            return jsonify({
                'success': False,
                'error': 400,
                'message': 'Title and release_date must be submitted.'
            }), 400

        new_movie = Movie(
            title=title,
            release_date=release_date
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
    """An endpoint to handle DELETE request '/movie/<int:movie_id>'

    Delete the corresponding row for movie_id. Only users with proper
    permission can delete movie.

    Arguments:
        payload (dict): decoded jwt payload
        movie_id (int): movie id which is wanted to delete
    Returns:
        Status code 200 and json object with
            "success": True or False
            'deleted': the deleted movie's id
            'total_movies': the number of remained movie after
                            deletion
    Raises:
        404: Resource is not found if the movie in the request is
            not existed.
        422: Request is unprocessable.
    """
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)

    try:
        movie.delete()
        all_movies = Movie.query.all()

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
    """An endpoint to handle PATCH request '/movie/<int:movie_id>'

    Update the title or release_date of the movie with provided id.
    It is permitted for users who have the proper validations.

    Arguments:
        payload (dict): decoded jwt payload
        movie_id (int): movie id which is wanted to patch
    Returns:
        Status code 200 and json object with
            "success": True or False
            "movie": a json object containing the updated movie data
    Raises:
        404: Resource is not found if the movie in request is not existed.
        422: Request is unprocessable.
    """
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)

    body = request.get_json()

    title = body.get('title', None)
    if title is not None:
        movie.title = title
    release_date = body.get('release_date', None)
    if release_date is not None:
        movie.release_date = release_date

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
    """An endpoint to handle GET requests '/actors'

    Retrieve a list of all actors from database

    Return:
        Status code 200 and json object with
            "success": True or False
            "actors": the list of the actors
    Raises:
        404: Resource is not found if any actor is not existed.
    """
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
    """An endpoint to handle GET requests '/actor/<int:actor_id>'

    Retrieve the actor data with provided id from database

    Arguments:
        payload (dict): decoded jwt payload
        actor_id (int): actor id which is wanted to retrieve
    Return:
        Status code 200 and json object with
            "success": True or False
            "movie": json object of the actor's data
    Raises:
        404: Resource is not found if the actor with provided id is
            not existed.
    """
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
    """An endpoint to handle POST request '/actor'

    Add a new actor in the actors table when the request user have
    a proper permission.

    Arguments:
        payload (dict): decoded jwt payload
    Returns:
        Status code 200 and json object with
            "success": True or False
            "created": The id of newly creacted actor data
            "total_actors": The number of the actors after adding
                            new actor.
    Raises:
        400: Name, age, or gender has not been submitted.
        422: Request is unprocessable.
    """
    try:
        body = request.get_json()
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')
        if not name or not age or not gender:
            return jsonify({
                'success': False,
                'error': 400,
                'message': 'Name, age, and gender must be submitted.'
            }), 400

        new_actor = Actor(name=name, age=age, gender=gender)
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
    """An endpoint to handle DELETE request '/actor/<int:actor_id>'

    Delete the corresponding row for actor_id. Only users with proper
    permission can delete actor.

    Arguments:
        payload (dict): decoded jwt payload
        actor_id (int): actor id which is wanted to delete
    Returns:
        Status code 200 and json object with
            "success": True or False
            'deleted': the deleted actor's id
            'total_actors': the number of remained actor after
                            deletion
    Raises:
        404: Resource is not found if the actor in the request is
            not existed.
        422: Request is unprocessable.
    """
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)

    try:
        actor.delete()
        all_actors = Actor.query.all()

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
    """An endpoint to handle PATCH request '/actor/<int:actor_id>'

    Update the name, age, or gender of the actor with provided id.
    It is permitted for users who have the proper validations.

    Arguments:
        payload (dict): decoded jwt payload
        actor_id (int): actor id which is wanted to patch
    Returns:
        Status code 200 and json object with
            "success": True or False
            "actor": a json object containing the updated actor data
    Raises:
        404: Resource is not found if the actor in request is not existed.
        422: Request is unprocessable.
    """
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)

    body = request.get_json()
    name = body.get('name', None)
    if name is not None:
        actor.name = name
    age = body.get('age', None)
    if age is not None:
        actor.age = age
    gender = body.get('gender', None)
    if gender is not None:
        actor.gender = gender

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
