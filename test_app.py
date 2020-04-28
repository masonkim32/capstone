import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db


class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        database_path = os.environ['TEST_DATABASE_URL']
        setup_db(self.app, database_path)

        self.casting_assistant = os.environ['CASTING_ASSISTANT']
        self.casting_director = os.environ['CASTING_DIRECTOR']
        self.executive_producer = os.environ['EXECUTIVE_PRODUCER']

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    # ===============================================================
    # TEST GET methods
    # ===============================================================

    def test_get_all_movies(self):
        response = self.client().get("/movies")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def test_get_all_actors(self):
        response = self.client().get("/actors")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def test_get_single_movie(self):
        response = self.client().get(
            "/movie/1",
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    def test_get_single_actor(self):
        response = self.client().get(
            "/actor/1",
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

    def test_401_get_single_movie_with_no_permission(self):
        response = self.client().get("/movie/1")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertEqual(data["message"], "Not authorized")

    def test_401_get_single_actor_with_no_permission(self):
        response = self.client().get("/actor/1")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertEqual(data["message"], "Not authorized")

    # ===============================================================
    # TEST POST methods
    # ===============================================================

    def test_add_movie(self):
        response = self.client().post(
            "/movie",
            json={
                "title": "Test Movie",
                "release_date": "04.28.2020"
            },
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_add_actor(self):
        response = self.client().post(
            "/actor",
            json={
                "name": "Test Actor",
                "age": 20,
                "gender": "male"
            },
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

    def test_401_add_movie_as_casting_assistant(self):
        response = self.client().post(
            "/movie",
            json={
                "title": "Test Movie",
                "release_date": "05.28.2020"
            },
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertEqual(data["message"], "Not authorized")

    def test_401_add_actor_as_casting_assistant(self):
        response = self.client().post(
            "/actor",
            json={
                "name": "Test Actor",
                "age": 24,
                "gender": "female"
            },
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertEqual(data["message"], "Not authorized")

    # ===============================================================
    # TEST PATCH methods
    # ===============================================================

    def test_update_movie(self):
        response = self.client().patch(
            "/movie/5",
            json={
                "title": "Patched Movie",
                "release_date": "05.28.2020"
            },
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movie"])

    def test_401_update_movie_as_casting_assistant(self):
        response = self.client().patch(
            "/movie/5",
            json={
                "title": "Patched Movie",
                "release_date": "05.28.2020"
            },
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertEqual(data["message"], "Not authorized")

    def test_404_update_movie_does_not_exist(self):
        response = self.client().patch(
            "/movie/200",
            json={
                "title": "Patched Movie",
                "release_date": "05.28.2020"
            },
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_update_actor(self):
        response = self.client().patch(
            "/actor/5",
            json={
                "age": 55,
                "gender": "male"
            },
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actor"])

    def test_401_update_actor_as_casting_assistant(self):
        response = self.client().patch(
            "/actor/5",
            json={
                "age": 55,
                "gender": "male"
            },
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertEqual(data["message"], "Not authorized")

    def test_404_update_actor_does_not_exist(self):
        response = self.client().patch(
            "/actor/200",
            json={
                "age": 55,
                "gender": "male"
            },
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    # ===============================================================
    # TEST DELETE methods
    # ===============================================================

    def test_delete_movie(self):
        response = self.client().delete(
            "/movie/2",
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"])

    def test_401_delete_movie_as_casting_director(self):
        response = self.client().delete(
            "/movie/4",
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertEqual(data["message"], "Not authorized")

    def test_404_delete_movie_does_not_exist(self):
        response = self.client().delete(
            "/movie/200",
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")

    def test_delete_actor(self):
        response = self.client().delete(
            "/actor/2",
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted"])

    def test_401_delete_actor_as_casting_assistant(self):
        response = self.client().delete(
            "/actor/4",
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            }
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 401)
        self.assertEqual(data["message"], "Not authorized")

    def test_404_delete_actor_does_not_exist(self):
        response = self.client().delete(
            "/actor/200",
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "resource not found")


if __name__ == "__main__":
    unittest.main()
