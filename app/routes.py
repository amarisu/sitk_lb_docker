from flask import current_app as app
from flask import jsonify, request
from .models import User, Task
from . import db

# Маршрут для создания нового пользователя
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get('username'):
        return jsonify({'message': 'Username is required.'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists.'}), 400
    user = User(username=data['username'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username}), 201

# Маршрут для получения списка всех пользователей
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users])

# Маршрут для получения задач конкретного пользователя
@app.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': task.id, 'description': task.description, 'completed': task.completed} for task in tasks])

# Маршрут для добавления новой задачи пользователю
@app.route('/users/<int:user_id>/tasks', methods=['POST'])
def add_task(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    data = request.get_json()
    if not data or not data.get('description'):
        return jsonify({'message': 'Task description is required.'}), 400
    task = Task(description=data['description'], user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id, 'description': task.description, 'completed': task.completed}), 201

# Маршрут для обновления статуса задачи (завершена/не завершена)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found.'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided.'}), 400
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify({'id': task.id, 'description': task.description, 'completed': task.completed})

# Маршрут для удаления задачи
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': 'Task not found.'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': f'Task {task.id} deleted.'}), 200
