import unittest
from main import app, db, User, Todo

class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = db

    def test_register(self):
        response = self.app.post('/register', json={'email': 'test@test.com', 'password': 'test'})
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = self.app.post('/login', json={'email': 'test@test.com', 'password': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_create_todo(self):
        response = self.app.post('/todos', json={'title': 'Test', 'description': 'Test description'}, headers={'Authorization': 'Bearer <token>'})
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()