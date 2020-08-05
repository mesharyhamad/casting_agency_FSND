import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Movie, Actor, setup_db

JWT_TEST_APP = open('JWT_TEST_APP.json', )
tokens = json.load(JWT_TEST_APP)
mock_actor_id = None
mock_actor2_id = None
mock_movie_id = None
mock_movie2_id = None


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "agency_test"
        self.database_path = os.environ.get('DATABASE_URL')
        setup_db(self.app, self.database_path)

        actor = Actor(name='Test_actor', age=30, gender='M')
        actor.insert()
        actor2 = Actor(name='Test_actor_2', age=30, gender='F')
        actor2.insert()
        global mock_actor_id, mock_actor2_id
        mock_actor_id = actor.id
        mock_actor2_id = actor2.id
        movie = Movie(title='Test_movie', release="2020-01-01")
        movie.insert()
        movie2 = Movie(title='Test_movie_2', release="2020-03-01")
        movie2.insert()
        global mock_movie_id, mock_movie2_id
        mock_movie_id = movie.id
        mock_movie2_id = movie2.id
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    test cases endpoint
    """

    # Permission of assistant and status code 200 to get actors
    def test_permission_assistant_to_get_actors_status_code_200(self):
        assistant_token = tokens['assistant_token']
        response = self.client().get('/actors', headers={'Authorization': f'Bearer {assistant_token}'})
        self.assertEqual(response.status_code, 200)

    # Permission of assistant and status code 401 to get actors
    def test_permission_assistant_to_get_actors_status_code_401(self):
        response = self.client().get('/actors')
        self.assertEqual(response.status_code, 401)

    # Permission of assistant and status code 200 to get movies
    def test_permission_assistant_to_get_movies_with_status_code_200(self):
        assistant_token = tokens['assistant_token']
        response = self.client().get('/movies', headers={'Authorization': f'Bearer {assistant_token}'})
        self.assertEqual(response.status_code, 200)

    # Permission of assistant and status code 401 to get movies
    def test_permission_assistant_to_get_movies_with_status_code_401(self):
        response = self.client().get('/movies')
        self.assertEqual(response.status_code, 401)

    # Permission not found in JWT with assistant role
    def test_not_permission_assistant_to_delete_movies_with_status_code_401(self):
        assistant_token = tokens['assistant_token']
        response = self.client().delete('/movies/1', headers={'Authorization': f'Bearer {assistant_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message'], "Permission not found in JWT")

    # Permission director to delete actors and test case status code 200
    def test_permission_director_to_delete_actors_with_status_code_200(self):
        director_token = tokens['director_token']
        global mock_actor_id

        response = self.client().delete(f'/actors/{mock_actor_id}', content_type='application/json',
                                        headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    # Permission director to delete actors and test case status code 404
    def test_permission_director_to_delete_actors_with_status_code_404(self):
        director_token = tokens['director_token']
        response = self.client().delete('/actors/11111111111', content_type='application/json',
                                        headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

    # Permission of director to create actor and test case status ok 200
    def test_permission_director_to_post_actor_with_status_200(self):
        director_token = tokens['director_token']
        response = self.client().post('/actors', data=json.dumps({
            'name': 'CHRIS EVANS',
            'age': '39',
            'gender': 'M',
        }), content_type='application/json', headers={'Authorization': f'Bearer {director_token}'})
        data = json.loads(response.data)
        global mock_actor_id
        mock_actor_id = data['actor']['id']
        self.assertEqual(response.status_code, 200)

    # Permission of director to create actor and  test case status 422
    def test_permission_director_to_post_actor_with_status_422(self):
        director_token = tokens['director_token']
        response = self.client().post('/actors', data=json.dumps({
        }), content_type='application/json', headers={'Authorization': f'Bearer {director_token}'})
        self.assertEqual(response.status_code, 422)

    # Permission of director to update actor and  test case status 200
    def test_permission_director_to_update_actor_with_status_200(self):
        director_token = tokens['director_token']
        global mock_actor2_id
        response = self.client().patch(f'/actors/{mock_actor2_id}', data=json.dumps({
            'name': 'update_test'
        }), content_type='application/json', headers={'Authorization': f'Bearer {director_token}'})
        self.assertEqual(response.status_code, 200)

    # Permission of director to update actor and  test case status 404
    def test_permission_director_to_update_actor_with_status_404(self):
        director_token = tokens['director_token']
        response = self.client().patch('/actors/1111111111111111', data=json.dumps({
            'name': 'update_test'
        }), content_type='application/json', headers={'Authorization': f'Bearer {director_token}'})
        self.assertEqual(response.status_code, 404)

    # Permission of director to update actor and  test case status 400
    def test_permission_director_to_update_actor_with_status_400(self):
        director_token = tokens['director_token']
        global mock_actor2_id
        response = self.client().patch(f'/actors/{mock_actor2_id}', content_type='application/json',
                                       headers={'Authorization': f'Bearer {director_token}'})
        self.assertEqual(response.status_code, 400)

    # Permission of executive_producer to create movie and  test case status 200
    def test_permission_executive_producer_to_create_movie_with_status_200(self):
        executive_producer_token = tokens['executive_producer_token']
        response = self.client().post('/movies', data=json.dumps({'title': 'test_title_post', 'release': '2020-01-01'
                                                                  }), content_type='application/json',
                                      headers={'Authorization': f'Bearer {executive_producer_token}'})
        self.assertEqual(response.status_code, 200)

    # Permission of executive_producer to create movie and  test case status 400
    def test_permission_executive_producer_to_create_movie_with_status_400(self):
        executive_producer_token = tokens['executive_producer_token']
        response = self.client().post('/movies', content_type='application/json',
                                      headers={'Authorization': f'Bearer {executive_producer_token}'})
        self.assertEqual(response.status_code, 400)

    # Permission of executive_producer to update movie and  test case status 200
    def test_permission_executive_producer_to_update_movie_with_status_200(self):
        executive_producer_token = tokens['executive_producer_token']
        response = self.client().patch(f'/movies/{mock_movie2_id}', data=json.dumps({'title': 'test_title_update'}),
                                       content_type='application/json',
                                       headers={'Authorization': f'Bearer {executive_producer_token}'})
        self.assertEqual(response.status_code, 200)

    # Permission of executive_producer to update movie and  test case status 404
    def test_permission_executive_producer_to_update_movie_with_status_404(self):
        executive_producer_token = tokens['executive_producer_token']
        response = self.client().patch('/movies/55555505', data=json.dumps({'title': 'test_title_update'}),
                                       content_type='application/json',
                                       headers={'Authorization': f'Bearer {executive_producer_token}'})
        self.assertEqual(response.status_code, 404)

    # Permission of executive_producer to delete movie and  test case status 200
    def test_permission_executive_producer_to_update_movie_with_status_200(self):
        executive_producer_token = tokens['executive_producer_token']
        response = self.client().delete(f'/movies/{mock_movie_id}', content_type='application/json',
                                        headers={'Authorization': f'Bearer {executive_producer_token}'})
        self.assertEqual(response.status_code, 200)

    # Permission of executive_producer to delete movie and  test case status 404
    def test_permission_executive_producer_to_update_movie_with_status_404(self):
        executive_producer_token = tokens['executive_producer_token']
        response = self.client().delete('/movies/88888888', content_type='application/json',
                                        headers={'Authorization': f'Bearer {executive_producer_token}'})
        self.assertEqual(response.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
