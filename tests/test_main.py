import unittest
from main import app, db, User, ToDo

class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = db

    def test_register(self):
        response = self.app.post('/api/register', json={'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        response = self.app.post('/api/login', json={'username': 'test', 'password': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_create_todo(self):
        response = self.app.post('/api/todo', json={'title': 'Test to-do', 'description': 'This is a test to-do', 'due_date': '2022-12-31', 'user_id': 1})
        self.assertEqual(response.status_code, 201)

    def test_get_todo(self):
        response = self.app.get('/api/todo/1')
        self.assertEqual(response.status_code, 200)

    def test_update_todo(self):
        response = self.app.put('/api/todo/1', json={'title': 'Updated test to-do', 'description': 'This is an updated test to-do', 'due_date': '2022-12-31', 'completion_status': true})
        self.assertEqual(response.status_code, 200)

    def test_delete_todo(self):
        response = self.app.delete('/api/todo/1')
        self.assertEqual(response.status_code, 200)

    def test_get_todos(self):
        response = self.app.get('/api/todos')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()