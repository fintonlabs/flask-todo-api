from flask import Flask, request, jsonify
import sqlite3
from sqlite3 import Error
from typing import Tuple

app = Flask(__name__)

DATABASE = 'todo.db'


def create_connection(db_file: str) -> sqlite3.Connection:
    """
    Create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_table(conn: sqlite3.Connection) -> None:
    """
    Create tasks table
    :param conn: Connection object
    :return: None
    """
    try:
        sql_create_tasks_table = """ CREATE TABLE IF NOT EXISTS tasks (
                                        id integer PRIMARY KEY,
                                        title text NOT NULL,
                                        description text,
                                        completed boolean NOT NULL DEFAULT 0,
                                        due_date date
                                    ); """
        conn.execute(sql_create_tasks_table)
    except Error as e:
        print(e)


@app.route('/tasks', methods=['GET'])
def get_tasks() -> Tuple[str, int]:
    """
    Get all tasks
    :return: JSON response
    """
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")

    rows = cur.fetchall()

    return jsonify(rows), 200


@app.route('/tasks', methods=['POST'])
def create_task() -> Tuple[str, int]:
    """
    Create a new task
    :return: JSON response
    """
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'the new task needs a title'}), 400

    task = (request.json.get('title', ""), request.json.get('description', ""), request.json.get('completed', 0),
            request.json.get('due_date', None))

    sql = ''' INSERT INTO tasks(title,description,completed,due_date)
              VALUES(?,?,?,?) '''
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

    return jsonify({'message': 'new task created'}), 201


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id: int) -> Tuple[str, int]:
    """
    Get a specific task
    :param task_id: ID of the task
    :return: JSON response
    """
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))

    row = cur.fetchone()

    if row is None:
        return jsonify({'error': 'task not found'}), 404

    return jsonify(row), 200


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id: int) -> Tuple[str, int]:
    """
    Update a specific task
    :param task_id: ID of the task
    :return: JSON response
    """
    if not request.json:
        return jsonify({'error': 'the updated task needs a title'}), 400

    task = (request.json.get('title', ""), request.json.get('description', ""), request.json.get('completed', 0),
            request.json.get('due_date', None), task_id)

    sql = ''' UPDATE tasks
              SET title = ? ,
                  description = ? ,
                  completed = ? ,
                  due_date = ?
              WHERE id = ?'''
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

    return jsonify({'message': 'task updated'}), 200


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int) -> Tuple[str, int]:
    """
    Delete a specific task
    :param task_id: ID of the task
    :return: JSON response
    """
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()

    return jsonify({'message': 'task deleted'}), 200


if __name__ == '__main__':
    conn = create_connection(DATABASE)
    if conn is not None:
        create_table(conn)
    else:
        print("Error! cannot create the database connection.")
    app.run(debug=True)