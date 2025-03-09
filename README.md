# Flask To-Do List API

This is a Flask API for a to-do list application. The application interacts with a SQLite database to store, retrieve, update, and delete to-do items.

## Installation

1. Clone the repository: `git clone https://github.com/yourusername/flask-todo-api.git`
2. Navigate to the project directory: `cd flask-todo-api`
3. Install the requirements: `pip install -r requirements.txt`

## Usage

Run the application: `python main.py`

The API has the following endpoints:

- GET /tasks: Retrieve all tasks
- POST /tasks: Create a new task
- GET /tasks/<id>: Retrieve a task by its ID
- PUT /tasks/<id>: Update a task by its ID
- DELETE /tasks/<id>: Delete a task by its ID