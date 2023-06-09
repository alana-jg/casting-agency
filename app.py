import os
from flask import Flask, jsonify, abort, request
from models import *
from flask_cors import CORS
from flask_migrate import Migrate
from auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    migrate = Migrate(app, db)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,DELETE,OPTIONS")
        return response

    @app.route('/')
    def home():
        return jsonify({'success': True}), 200

    #------ACTORS------

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):
        try:
            actors = Actor.query.order_by(Actor.id).all()
            format_actors = [actor.format() for actor in actors]

            return jsonify({
                'success' : True,
                'actors' : format_actors
            }), 200
        except Exception as e:
            print(e)
            abort(500)


    @app.route('/actors', methods = ['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
         
        actor = request.get_json()

        if "name" not in actor or "age" not in actor or "gender" not in actor:
            abort(400)

        try:
            name = actor.get("name")
            age = actor.get("age")
            gender = actor.get("gender")

            new_actor = Actor(
                name = name,
                age = age,
                gender = gender
            )
            db.session.add(new_actor)
            db.session.commit()

            return jsonify ({
                'success' : True,
                'name' : name,
                'age' : age,
                'gender' : gender
             }), 201
        except:
            db.session.rollback()
            abort(500)
        finally: 
            db.session.close()


    @app.route('/actors/<int:actor_id>', methods = ['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, actor_id):
        actor = Actor.query.get_or_404(actor_id)

        new_actor = request.get_json()

        name = new_actor.get("name", None)
        age = new_actor.get("age", None)
        gender = new_actor.get("gender", None)

        if name is None or age is None or gender is None:
            abort(400)

        try:
            actor.name = name
            actor.age = age
            actor.gender = gender
            actor.update()

            return jsonify ({
                'success' : True,
                'name' : name,
                'age' : age,
                'gender' : gender
             }), 201
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    @app.route('/actors/<int:actor_id>', methods = ['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        actor = Actor.query.get_or_404(actor_id)

        try:
            actor.delete()

            return jsonify({
                "success" : True,
                "name" : actor.name,
                "deleted" : actor_id
            }), 201
        except:
            abort (422)


    #------MOVIES------

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        try:
            movies = Movie.query.order_by(Movie.id).all()
            format_movies = [movie.format() for movie in movies]

            return jsonify({
                'success' : True,
                'movies' : format_movies
            }), 200
        except Exception as e:
            print(e)
            abort(500)

    @app.route('/movies', methods = ['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        movie = request.get_json()

        if "title" not in movie or "release_date" not in movie:
            abort(400)

        try:
            title = movie.get("title")
            release_date = movie.get("release_date")

            new_movie = Movie(
                title = title,
                release_date = release_date
            )
            db.session.add(new_movie)
            db.session.commit()

            return jsonify ({
                'success' : True,
                'title' : title,
                'release_date' : release_date
             }), 201
        except:
            db.session.rollback()
            abort(500)
        finally: 
            db.session.close()

    @app.route('/movies/<int:movie_id>', methods = ['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, movie_id):
        movie = Movie.query.get_or_404(movie_id)

        new_movie = request.get_json()

        title = new_movie.get("title", None)
        release_date = new_movie.get("release_date", None)

        if title is None or release_date is None:
            abort(400)

        try:
            movie.title = title
            movie.release_date = release_date
            movie.update()

            return jsonify ({
                'success' : True,
                'title' : title,
                'release_date' : release_date
             }), 201
        except Exception as e:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    @app.route('/movies/<int:movie_id>', methods = ['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        movie = Movie.query.get_or_404(movie_id)

        try:
            movie.delete()

            return jsonify({
                "success" : True,
                "title" : movie.title,
                "deleted" : movie_id
            }), 201
        except:
            abort (422)




#------ERROR FORMATTING------

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({
                'error' : 400,
                'success' : False,
                'message' : 'bad request'
            }), 
            400)

    @app.errorhandler(401)
    def unauthorised(error):

        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorised for this action'
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({
                'error' : 404,
                'success' : False,
                'message' : 'resource not found'
            }),
            404)

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({
                'error' : 422,
                'success' : False,
                'message' : 'unprocessable'
            }),
            422)

    @app.errorhandler(500)
    def unprocessable(error):
        return (
            jsonify({
                'error' : 500,
                'success' : False,
                'message' : 'an unexpected error occured, request could not be processed'
            }),
            500)

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success" : False,
            "error" : error.status_code,
            "message" : error.error
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
