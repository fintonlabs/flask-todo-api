import unittest
from main import app, db, Task

class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = db

    def test_get_tasks(self):
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        response = self.app.post('/tasks', json={'title': 'Test Task', 'description': 'Test Description'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['title'], 'Test Task')
        self.assertEqual(data['description'], 'Test Description')

    def test_get_task(self):
        task = Task(title='Test Task', description='Test Description')
        self.db.session.add(task)
        self.db.session.commit()
        response = self.app.get(f'/tasks/{task.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Test Task')
        self.assertEqual(data['description'], 'Test Description')

    def test_update_task(self):
        task = Task(title='Test Task', description='Test Description')
        self.db.session.add(task)
        self.db.session.commit()
        response = self.app.put(f'/tasks/{task.id}', json={'title': 'Updated Task', 'description': 'Updated Description'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Updated Task')
        self.assertEqual(data['description'], 'Updated Description')

    def test_delete_task(self):
        task = Task(title='Test Task', description='Test Description')
        self.db.session.add(task)
        self.db.session.commit()
        response = self.app.delete(f'/tasks/{task.id}')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()