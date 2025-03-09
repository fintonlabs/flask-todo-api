from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(80))
    auth_token = db.Column(db.String(200))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(200))
    completed = db.Column(db.Boolean)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/tasks', methods=['GET'])
@token_required
def get_all_tasks(current_user):
    tasks = Task.query.all()
    output = []
    for task in tasks:
        task_data = {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}
        output.append(task_data)
    return jsonify({'tasks': output})

@app.route('/tasks/<id>', methods=['GET'])
@token_required
def get_one_task(current_user, id):
    task = Task.query.filter_by(id=id).first()
    if not task:
        return jsonify({'message': 'No task found!'})
    task_data = {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}
    return jsonify(task_data)

@app.route('/tasks', methods=['POST'])
@token_required
def create_task(current_user):
    data = request.get_json()
    new_task = Task(title=data['title'], description=data['description'], completed=False)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'New task created!'})

@app.route('/tasks/<id>', methods=['PUT'])
@token_required
def complete_task(current_user, id):
    task = Task.query.filter_by(id=id).first()
    if not task:
        return jsonify({'message': 'No task found!'})
    task.completed = True
    db.session.commit()
    return jsonify({'message': 'Task has been completed!'})

@app.route('/tasks/<id>', methods=['DELETE'])
@token_required
def delete_task(current_user, id):
    task = Task.query.filter_by(id=id).first()
    if not task:
        return jsonify({'message': 'No task found!'})
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task has been deleted!'})

if __name__ == '__main__':
    app.run(debug=True)