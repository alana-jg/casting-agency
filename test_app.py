import os
from os.path import join, dirname
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'login.env')
load_dotenv(dotenv_path)

casting_assistant_token = os.environ.get('CASTING_ASSISTANT')
casting_director_token = os.environ.get('CASTING_DIRECTOR')
executive_producer_token = os.environ.get('EXECUTIVE_PRODUCER')

class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_user = os.getenv('USER')
        self.database_password = os.getenv('PASSWORD')
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(self.database_user, self.database_password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.headers_casting_assistant = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + casting_assistant_token
        }

        self.headers_casting_director = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + casting_director_token
        }

        self.headers_executive_producer = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + executive_producer_token
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.new_actor = {
            'name': 'Emma Watson',
            'age':33,
            'gender': 'female'
        }

        self.new_actor_2 = {
            'name': 'Maggie Smith',
            'age':88,
            'gender': 'female'
        }

        self.incomplete_actor = {
            'name': 'Seth Rogan',
            'age': 41
        }

        self.updated_actor = {
            'name': 'Emma Watson',
            'age':35,
            'gender': 'female'
        }

        self.new_movie = {
            'title':'Toy Story',
            'release_date': 1995
        }

        self.incomplete_movie = {
            'title': 'Monsters Inc'
        }

        self.updated_movie = {
            'title':'Toy Story',
            'release_date': 1997
        }

    def tearDown(self):
        pass


    def test_index_health(self):
        response = self.client().get("/")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)

#------ACTORS TESTS------

    #should pass with casting assistant token
    def test_get_actors(self):
        response = self.client().get('/actors', headers = self.headers_casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    #should pass with casting director token
    def test_post_new_actor(self):
        response = self.client().post('/actors', json = self.new_actor, headers = self.headers_casting_director)
        data = json.loads(response.data)

        actor = Actor.query.filter(Actor.name == data['name']).all()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['name'], self.new_actor['name'])
        self.assertEqual(data['age'], self.new_actor['age'])
        self.assertEqual(data['gender'], self.new_actor['gender'])
        self.assertIsNotNone(actor)

    #should fail with unauthorised casting assistant token
    def test_403_unauthorised_post_new_actor(self):
        response = self.client().post('/actors', json = self.new_actor, headers = self.headers_casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)

    #should fail with casting director token due to incomplete json input
    def test_404_incomplete_actor(self):
        response = self.client().post('/actors', json = self.incomplete_actor, headers = self.headers_casting_director)
        data = json.loads(response.data)

        actor = Actor.query.filter(Actor.name == self.incomplete_actor['name']).one_or_none()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        self.assertEqual(actor, None)

    #should pass with casting director token
    def test_update_actor(self):
        id = 11
        response = self.client().patch('/actors/{}'.format(id), json = self.updated_actor, headers = self.headers_casting_director)
        data = json.loads(response.data)

        actor = Actor.query.filter(Actor.name == self.updated_actor['name']).all()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['name'], self.updated_actor['name'])
        self.assertEqual(data['age'], self.updated_actor['age'])
        self.assertEqual(data['gender'], self.updated_actor['gender'])
        self.assertIsNotNone(actor)

    #should fail with unauthorised casting assistant token
    def test_403_unauthorised_update_actor(self):
        id = 11
        response = self.client().patch('/actors/{}'.format(id), json = self.updated_actor, headers = self.headers_casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)

    #should fail with casting director token due to invalid id
    def test_404_missing_update_actor(self):
        id = 1000
        response = self.client().patch('/actors/{}'.format(id), headers = self.headers_casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #should fail with casting director token due to incomplete json input
    def test_400_invalid_update_actor(self):
        id = 1
        response = self.client().patch('actors/{}'.format(id), json = self.incomplete_actor, headers = self.headers_casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    #should pass with casting director token
    def test_delete_actor(self):
        id = 18
        response = self.client().delete('/actors/{}'.format(id), headers = self.headers_casting_director)
        data = json.loads(response.data)

        actor = Actor.query.filter(Actor.id == id).one_or_none()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['name'])
        self.assertEqual(data['deleted'], id)
        self.assertEqual(actor, None)

    #should fail with unauthorised casting assistant token 
    def test_403_unauthorised_delete_actor(self):
        id = 15
        response = self.client().delete('/actors/{}'.format(id), headers = self.headers_casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)

    #should fail with casting director token due to invalid id
    def test_404_invalid_delete_actor(self):
        id = 9000
        response = self.client().delete('/actors/{}'.format(id), headers = self.headers_casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

#------MOVIES TESTS------

    #should pass with casting assistant token
    def test_get_movies(self):
        response = self.client().get('/movies', headers = self.headers_casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    #should pass with executive producer token
    def test_post_new_movie(self):
        response = self.client().post('/movies', json = self.new_movie, headers = self.headers_executive_producer)
        data = json.loads(response.data)

        movie = Movie.query.filter(Movie.title == data['title']).all()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['title'], self.new_movie['title'])
        self.assertEqual(data['release_date'], self.new_movie['release_date'])
        self.assertIsNotNone(movie)

    #should fail with unauthorised casting director token
    def test_403_unauthorised_post_new_movie(self):
        response = self.client().post('/movies', json = self.new_movie, headers = self.headers_casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)

    #should fail with executive producer token due to incomplete json input
    def test_404_incomplete_movie(self):
        response = self.client().post('/movies', json = self.incomplete_movie, headers = self.headers_executive_producer)
        data = json.loads(response.data)

        movie = Movie.query.filter(Movie.title == self.incomplete_movie['title']).one_or_none()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        self.assertEqual(movie, None)

    #should pass with casting director token
    def test_update_movie(self):
        id = 2
        response = self.client().patch('/movies/{}'.format(id), json = self.updated_movie, headers = self.headers_casting_director)
        data = json.loads(response.data)

        movie = Movie.query.filter(Movie.title == self.updated_movie['title']).all()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['title'], self.updated_movie['title'])
        self.assertEqual(data['release_date'], self.updated_movie['release_date'])
        self.assertIsNotNone(movie)

    #should fail due to unauthorised casting assistant token
    def test_403_unauthorised_update_movie(self):
        id = 2
        response = self.client().patch('/movies/{}'.format(id), json = self.updated_movie, headers = self.headers_casting_assistant)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)

    #should fail with casting director token due to invalid id
    def test_404_missing_update_movie(self):
        id = 1000
        response = self.client().patch('/movies/{}'.format(id), headers = self.headers_casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #should fail with casting director token due to invalid json input
    def test_400_invalid_update_movie(self):
        id = 3
        response = self.client().patch('movies/{}'.format(id), json = self.incomplete_movie, headers = self.headers_casting_director)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    #should pass with executive producer token
    def test_delete_movie(self):
        id = 7
        response = self.client().delete('/movies/{}'.format(id), headers = self.headers_executive_producer)
        data = json.loads(response.data)

        movie = Movie.query.filter(Movie.id == id).one_or_none()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['title'])
        self.assertEqual(data['deleted'], id)
        self.assertEqual(movie, None)

    #should fail with unauthorised casting director token
    def test_403_unauthorised_delete_movie(self):
        id = 5
        response = self.client().delete('/movies/{}'.format(id), headers = self.headers_casting_director)
        data = json.loads(response.data)  

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)      

    #should fail with executive producer token due to invalid id
    def test_404_invalid_delete_movie(self):
        id = 9000
        response = self.client().delete('/movies/{}'.format(id), headers = self.headers_executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

if __name__ == "__main__":
    unittest.main()