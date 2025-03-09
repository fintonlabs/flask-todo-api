from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(200))
    status = db.Column(db.String(50), default='pending')
    user_id = db.Column(db.Integer)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorator

@app.route('/tasks', methods=['GET'])
@token_required
def get_all_tasks(current_user):
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    output = []
    for task in tasks:
        task_data = {}
        task_data['id'] = task.id
        task_data['title'] = task.title
        task_data['description'] = task.description
        task_data['status'] = task.status
        output.append(task_data)
    return jsonify({'tasks': output})

@app.route('/tasks/<task_id>', methods=['GET'])
@token_required
def get_one_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'message': 'No task found!'})
    task_data = {}
    task_data['id'] = task.id
    task_data['title'] = task.title
    task_data['description'] = task.description
    task_data['status'] = task.status
    return jsonify(task_data)

@app.route('/tasks', methods=['POST'])
@token_required
def create_task(current_user):
    data = request.get_json()
    new_task = Task(title=data['title'], description=data['description'], status=data['status'], user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'New task created!'})

@app.route('/tasks/<task_id>', methods=['PUT'])
@token_required
def complete_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'message': 'No task found!'})
    data = request.get_json()
    task.title = data['title']
    task.description = data['description']
    task.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Task has been updated!'})

@app.route('/tasks/<task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'message': 'No task found!'})
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task has been deleted!'})

if __name__ == '__main__':
    app.run(debug=True)