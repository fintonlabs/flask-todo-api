# Flask To-Do List API

This is a Flask API for a to-do list application. The application interacts with a SQLite database to store, retrieve, update, and delete to-do items.

## Installation

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt`
3. Run the application with `python main.py`

## Usage

- Get all tasks: `GET /tasks`
- Get one task: `GET /tasks/<task_id>`
- Create a task: `POST /tasks` with JSON body `{ "title": "task title", "description": "task description", "due_date": "YYYY-MM-DD" }`
- Update a task: `PUT /tasks/<task_id>` with JSON body `{ "title": "task title", "description": "task description", "due_date": "YYYY-MM-DD", "status": "task status" }`
- Delete a task: `DELETE /tasks/<task_id>`