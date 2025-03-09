import unittest
import main

class TestMain(unittest.TestCase):
    def setUp(self):
        main.app.testing = True
        self.app = main.app.test_client()

    def test_get_tasks(self):
        rv = self.app.get('/tasks')
        self.assertEqual(rv.status_code, 200)

    def test_create_task(self):
        rv = self.app.post('/tasks', json={'title': 'test task'})
        self.assertEqual(rv.status_code, 201)
        self.assertIn('new task created', rv.get_json()['message'])

    def test_get_task(self):
        rv = self.app.get('/tasks/1')
        self.assertEqual(rv.status_code, 200)

    def test_update_task(self):
        rv = self.app.put('/tasks/1', json={'title': 'updated task'})
        self.assertEqual(rv.status_code, 200)
        self.assertIn('task updated', rv.get_json()['message'])

    def test_delete_task(self):
        rv = self.app.delete('/tasks/1')
        self.assertEqual(rv.status_code, 200)
        self.assertIn('task deleted', rv.get_json()['message'])

if __name__ == '__main__':
    unittest.main()