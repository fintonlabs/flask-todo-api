from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # replace with your secret key

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    due_date = db.Column(db.DateTime, nullable=False)
    completion_status = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    token = create_access_token(identity=user.id)
    return jsonify({'access_token': token}), 200

@app.route('/api/todo', methods=['POST'])
@jwt_required()
def create_todo():
    data = request.get_json()
    new_todo = ToDo(title=data['title'], description=data['description'], due_date=datetime.strptime(data['due_date'], '%Y-%m-%d'), user_id=data['user_id'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'To-do created'}), 201

@app.route('/api/todo/<id>', methods=['GET'])
@jwt_required()
def get_todo(id):
    todo = ToDo.query.get(id)
    if not todo:
        return jsonify({'message': 'To-do not found'}), 404
    return jsonify({'title': todo.title, 'description': todo.description, 'due_date': todo.due_date.strftime('%Y-%m-%d'), 'completion_status': todo.completion_status}), 200

@app.route('/api/todo/<id>', methods=['PUT'])
@jwt_required()
def update_todo(id):
    data = request.get_json()
    todo = ToDo.query.get(id)
    if not todo:
        return jsonify({'message': 'To-do not found'}), 404
    todo.title = data['title']
    todo.description = data['description']
    todo.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
    todo.completion_status = data['completion_status']
    db.session.commit()
    return jsonify({'message': 'To-do updated'}), 200

@app.route('/api/todo/<id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    todo = ToDo.query.get(id)
    if not todo:
        return jsonify({'message': 'To-do not found'}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'To-do deleted'}), 200

@app.route('/api/todos', methods=['GET'])
@jwt_required()
def get_todos():
    todos = ToDo.query.all()
    output = []
    for todo in todos:
        todo_data = {'title': todo.title, 'description': todo.description, 'due_date': todo.due_date.strftime('%Y-%m-%d'), 'completion_status': todo.completion_status}
        output.append(todo_data)
    return jsonify({'todos': output}), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)