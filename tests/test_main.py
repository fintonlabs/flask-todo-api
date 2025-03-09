import unittest
from main import app, db, Task

class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = db

    def test_get_all_tasks(self):
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)

    def test_get_one_task(self):
        task = Task(title='Test Task', description='Test Description', status='pending')
        db.session.add(task)
        db.session.commit()
        response = self.app.get(f'/tasks/{task.id}')
        self.assertEqual(response.status_code, 200)

    def test_create_task(self):
        response = self.app.post('/tasks', json={'title': 'Test Task', 'description': 'Test Description', 'status': 'pending'})
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        task = Task(title='Test Task', description='Test Description', status='pending')
        db.session.add(task)
        db.session.commit()
        response = self.app.put(f'/tasks/{task.id}', json={'title': 'Updated Task', 'description': 'Updated Description', 'status': 'completed'})
        self.assertEqual(response.status_code, 200)

    def test_delete_task(self):
        task = Task(title='Test Task', description='Test Description', status='pending')
        db.session.add(task)
        db.session.commit()
        response = self.app.delete(f'/tasks/{task.id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()