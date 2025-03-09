from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Bad credentials'}), 401
    token = create_access_token(identity=user.id)
    return jsonify({'access_token': token}), 200


@app.route('/todos', methods=['POST'])
@jwt_required
def create_todo():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_todo = Todo(title=data['title'], description=data['description'], user_id=user_id)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo created'}), 201


@app.route('/todos', methods=['GET'])
@jwt_required
def get_todos():
    user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': todo.id, 'title': todo.title, 'description': todo.description, 'completed': todo.completed} for todo in todos])


@app.route('/todos/<int:id>', methods=['PUT'])
@jwt_required
def update_todo(id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=id, user_id=user_id).first()
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
    data = request.get_json()
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    db.session.commit()
    return jsonify({'message': 'Todo updated'})


@app.route('/todos/<int:id>', methods=['DELETE'])
@jwt_required
def delete_todo(id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=id, user_id=user_id).first()
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted'})


@app.route('/todos/<int:id>/complete', methods=['PATCH'])
@jwt_required
def complete_todo(id):
    user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=id, user_id=user_id).first()
    if not todo:
        return jsonify({'message': 'Todo not found'}), 404
    todo.completed = True
    db.session.commit()
    return jsonify({'message': 'Todo marked as complete'})


if __name__ == '__main__':
    if not os.path.exists('/tmp/test.db'):
        db.create_all()
    app.run(debug=True)