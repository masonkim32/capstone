# FLASK_APP=api.py FLASK_ENV=development flask run

import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .models import setup_db, Movie, Actor


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    return app


app = create_app()


@app.route('/movies', methods=['GET'])
def retrieve_movies():
    movies = Movie.query.all()
    if len(movies) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'movies': movies
    }), 200


@app.route('/movie/<int:movie_id>', methods=['GET'])
def retrieve_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)

    return jsonify({
        'success': True,
        'movie': movie
    })


@app.route('/movie', methods=['POST'])
def add_movies():
    try:
        body = request.get_json()

        new_movie = Movie(
            title=body.get('title'),
            release_date=('release_data', None)
        )
        new_movie.insert()

        all_movies = Movie.query.all()

        return jsonify({
            'success': True,
            'created': new_movie.id,
            'total_movies': len(all_movies),
        })
    except Exception:
        abort(422)


@app.route('/movie/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
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
        })

    except Exception:
        abort(422)


@app.route('/movie/<int:movie_id>', methods=['PATCH'])
def update_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)

    body = request.get_json()

    movie_title = body.get('title', None)
    if movie_title is not None:
        movie.title = movie_title
    movie_release_date = body.get('release_date', None)
    if movie_release_date is not None:
        movie.recipe = movie_release_date

    try:
        movie.update()
    except Exception as e:
        abort(422)

    return jsonify({
        'success': True,
        'movie': movie
    })


@app.route('/actors', methods=['GET'])
def retrieve_actors():
    actors = Actor.query.all()

    if len(actors) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'actors': actors
    }), 200


@app.route('/actor/<int:actor_id>', methods=['GET'])
def retrieve_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)

    return jsonify({
        'success': True,
        'actor': actor
    })


@app.route('/actor', methods=['POST'])
def add_actor():
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
        })
    except Exception:
        abort(422)


@app.route('/actor/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):
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
        })

    except Exception:
        abort(422)


@app.route('/actor/<int:actor_id>', methods=['PATCH'])
def update_actor(actor_id):
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
        'actor': actor
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
