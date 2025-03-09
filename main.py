from flask import Flask, request, jsonify
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

def create_connection():
    """Create a database connection to a SQLite database."""
    conn = None;
    try:
        conn = sqlite3.connect(':memory:')  # create a database in RAM
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    """Create a Tasks table in SQLite database."""
    try:
        sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS Tasks (
                                        id integer PRIMARY KEY,
                                        title text NOT NULL,
                                        description text NOT NULL,
                                        done boolean NOT NULL
                                    );"""
        conn.execute(sql_create_tasks_table)
    except Error as e:
        print(e)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks from the Tasks table."""
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tasks")
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task in the Tasks table."""
    conn = create_connection()
    cur = conn.cursor()
    task = request.get_json()
    cur.execute("INSERT INTO Tasks(title, description, done) VALUES(?,?,?)", (task['title'], task['description'], task['done']))
    conn.commit()
    return jsonify(task), 201

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    """Get a specific task by id from the Tasks table."""
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tasks WHERE id=?", (id,))
    row = cur.fetchone()
    return jsonify(row)

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    """Update a specific task by id in the Tasks table."""
    conn = create_connection()
    cur = conn.cursor()
    task = request.get_json()
    cur.execute("UPDATE Tasks SET title=?, description=?, done=? WHERE id=?", (task['title'], task['description'], task['done'], id))
    conn.commit()
    return jsonify(task)

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    """Delete a specific task by id from the Tasks table."""
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Tasks WHERE id=?", (id,))
    conn.commit()
    return '', 204

if __name__ == '__main__':
    conn = create_connection()
    if conn is not None:
        create_table(conn)
    else:
        print("Error! cannot create the database connection.")
    app.run(debug=True)