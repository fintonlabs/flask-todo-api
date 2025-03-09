import unittest
from main import app, db, Task

class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = db

    def test_get_all_tasks(self):
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        response = self.app.post('/tasks', json={
            'title': 'Test task',
            'description': 'Test description',
            'due_date': '2022-12-31'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'New task created!')

    # Add more tests as needed

if __name__ == '__main__':
    unittest.main()