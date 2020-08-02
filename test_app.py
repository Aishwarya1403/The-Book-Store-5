import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from app import create_app
from models import setup_db, Books, Categories
from auth import AuthError
import requests

load_dotenv('.env')

owner_token = "Bearer {}".format(os.environ.get('owner_token'))
keeper_token = "Bearer {}".format(os.environ.get('keeper_token'))


class BookshopTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.owner_token = owner_token
        self.keeper_token = keeper_token
        self.database_name = "bookstore"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_books(self):
        res= self.client().get('/', headers={
            "Authorization": "Bearer {}".format(os.environ.get('owner_token'))
            })
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["books"])

    def test_books_id(self):
        res=self.client().get('/categories/4', headers={
            "Authorization": "Bearer {}".format(os.environ.get('owner_token'))
            })
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"], True)

    def test_post_books(self):
        new_book={
            "name":"Godan",
            "author":"Munshi Premchand",
            "category":34
        }
        res=self.client().post('/categories/4', headers={
            "Authorization": "Bearer {}".format(os.environ.get('owner_token'))
        },json=new_book)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_deleteBook(self):
        res = self.client().delete('/categories/8', headers={
            "Authorization": "Bearer {}".format(os.environ.get('owner_token'))
          })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_patchBook(self):
        change = {
            "name":"Alchemist",
            "author":"Paulo Coehlo",
            "category":35
        }
        res = self.client().patch('/category/9', headers={
            "Authorization": "Bearer {}".format(os.environ.get('owner_token'))}, json = change)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)


    def test_404_on_bookById(self):
        res = self.client().get('/categories/1', headers={
            "Authorization": "Bearer {}".format(os.environ.get('owner_token'))
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"],"Not Found")

    def test_422_on_postBooks(self):
        new_book = {
            "name":"abc",
            "author":"xyz",
            "category_id":5
        }
        res = self.client().post('/categories/2',headers={
            "Authorization": "Bearer {}".format(os.environ.get('owner_token'))
            }, json=new_book)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable Entity")

    def test_403_on_delete(self):
        res = self.client().delete('/categories/9000',headers={
            "Authorization": "Bearer {}".format(os.environ.get('owner_token'))
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"],"Forbidden/Unauthorized")

    def test_500_on_patch(self):
        change = {
            "name":"abc",
            "name":100,
            "category_id": 1000
        }
        res = self.client().patch('/category/', headers={
            "Authorization": "Bearer {}".format(os.environ.get('owner_token'))
            }, json = change)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found")


######## ROLE-BASED TESTS FOR KEEPER ########

    def test_403_keeper_post(self):
        new_book={
            "name":"Godan",
            "author":"Munshi Premchand",
            "category":34
        }
        res=self.client().post('/categories/4', headers={
            "Authorization": "Bearer {}".format(os.environ.get('keeper_token'))
            },json=new_book)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 403)

    def test_keeper_get_books(self):
        res= self.client().get('/', headers={
            "Authorization": "Bearer {}".format(os.environ.get('keeper_token'))
            })
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["books"])

    def test_keeper_get_Books_id(self):
        res=self.client().get('/categories/4', headers={
            "Authorization": "Bearer {}".format(os.environ.get('keeper_token'))
            })
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"], True)

    def test_keeper_delete(self):
        res = self.client().delete('/categories/6', headers={
            "Authorization": "Bearer {}".format(os.environ.get('keeper_token'))
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        

if __name__ == "__main__":
    unittest.main()