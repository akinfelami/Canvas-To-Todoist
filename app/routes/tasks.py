from flask import Blueprint


tasks = Blueprint('tasks', __name__)

@tasks.route('/')
def user_index():
    return {'msg': 'Success', 'blueprint': 'tasks'}