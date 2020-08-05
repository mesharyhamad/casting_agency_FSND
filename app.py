import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Movie, Actor, setup_db
from auth.auth import *

import sys


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
     Set up CORS. Allow '*' for origins.
    '''
    CORS(app)

    '''
    Set Access-Control-Allow after_request decorator
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,PATCH,DELETE')
        return response

    '''
         GET /actors
         To fetches all available actors
          It should require the 'get:actors' permission
    '''

    @app.route('/', methods=['GET'])
    def list_actors():

        return jsonify({
            'success': True,
        }), 200

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(token):

        return jsonify({
            'success': True,
            'actors': list(map(lambda a: a.serialize(), Actor.query.all())),
        }), 200

    '''
        POST /actors
        it should create a new row in the actors table
        it should require the 'post:actors' permission
    '''

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(token):
        actor_data = request.get_json()
        if actor_data is None:
            abort(400)
        if not('name' in actor_data or 'age'
                in actor_data or 'gender' in actor_data):
            abort(422)
        try:
            actor = Actor(name=actor_data.get('name'),
                          age=actor_data.get('age'),
                          gender=actor_data.get('gender'))
            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.serialize(),
            }), 200
        except Exception:
            abort(500)

    '''
        PATCH /actors/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:actors' permission
    '''

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(token, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        actor_data = request.get_json()
        if actor_data is None:
            abort(400)
        try:
            if 'name' in actor_data and actor_data.get('name') is not None:
                actor.name = actor_data.get('name')

            if 'age' in actor_data and actor_data.get('age') is not None:
                actor.gender = actor_data.get('age')

            if 'gender' in actor_data and actor_data.get('gender') is not None:
                actor.gender = actor_data.get('age')

            actor.update()

            return jsonify({
                'success': True,
                'id': actor_id,
            }), 200

        except Exception:
            abort(500)

    '''
        DELETE /actors/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:actors' permission
    '''

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.delete()
        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'deleted_id': actor_id,
        }), 200

    '''
    GET /movies
    To fetches all available movies
    It should require the 'get:movies' permission
    '''

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(token):

        return jsonify({
            'success': True,
            'movies': list(map(lambda m: m.serialize(),
                               Movie.query.order_by(Movie.id).all())),
        }), 200

    '''
        POST /movies
        it should create a new row in the movies table
        it should require the 'post:movies' permission
    '''

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(token):

        movie_data = request.get_json()
        if movie_data is None:
            abort(400)
        if 'title' not in movie_data or 'release' not in movie_data:
            abort(422)
        try:
            movie = Movie(title=movie_data.get('title'),
                          release=movie_data.get('release'))
            movie.insert()
            return jsonify({
                'success': True,
                'movie': movie.serialize(),
            }), 200
        except Exception:
            abort(500)

    '''
        PATCH /movies/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should update the corresponding row for <id>
            it should require the 'patch:movies' permission
    '''

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(token, movie_id):

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        movie_data = request.get_json()
        if movie_data is None:
            abort(400)

        try:
            if 'title' in movie_data \
                    and movie_data.get('title') is not None:
                movie.title = movie_data.get('title')

            if 'release' in movie_data \
                    and movie_data.get('release') is not None:
                movie.release = movie_data.get('release')

            movie.update()

            return jsonify({
                'success': True,
                'movie_id': movie_id,
            }), 200

        except Exception:
            abort(500)

    '''
         DELETE /movies/<id>
             where <id> is the existing model id
             it should respond with a 404 error if <id> is not found
             it should delete the corresponding row for <id>
             it should require the 'delete:movies' permission
     '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(token, movie_id):

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)
        try:
            movie.delete()

            return jsonify({
                'success': True,
                'movie_id': movie_id,
            }), 200
        except Exception:
            abort(500)

    '''
    Create error handlers for all expected errors
    including 404 ,422 ,500 ,400.
    '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(400)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": " Bad Request"
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify(e.error), e.status_code

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run()
