# 📝 Flask To-Do List API 📝

This is a Flask API for a to-do list application. The application interacts with a SQLite database to store and retrieve to-do items.

## 🐾 Author: Finton the DevopsDog 🐾

## 🚀 Installation 🚀

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt`
3. Run the application with `python main.py`

## 🎯 Usage 🎯

- Get all tasks: `GET /tasks`
- Create a new task: `POST /tasks`
- Get a specific task: `GET /tasks/<task_id>`
- Update a specific task: `PUT /tasks/<task_id>`
- Delete a specific task: `DELETE /tasks/<task_id>`

## 🧪 Testing 🧪

Run the tests with `python -m unittest tests/test_main.py`