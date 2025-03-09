import unittest
import main

class TestMain(unittest.TestCase):

    def setUp(self):
        self.app = main.app.test_client()
        self.app.testing = True 

    def test_get_tasks(self):
        result = self.app.get('/tasks')
        self.assertEqual(result.status_code, 200)

    def test_create_task(self):
        task = {
            'title': 'Test Task',
            'description': 'Test Description',
            'done': False
        }
        result = self.app.post('/tasks', json=task)
        self.assertEqual(result.status_code, 201)

    def test_get_task(self):
        result = self.app.get('/tasks/1')
        self.assertEqual(result.status_code, 200)

    def test_update_task(self):
        task = {
            'title': 'Updated Test Task',
            'description': 'Updated Test Description',
            'done': True
        }
        result = self.app.put('/tasks/1', json=task)
        self.assertEqual(result.status_code, 200)

    def test_delete_task(self):
        result = self.app.delete('/tasks/1')
        self.assertEqual(result.status_code, 204)

if __name__ == "__main__":
    unittest.main()