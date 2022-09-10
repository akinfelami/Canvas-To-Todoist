from re import T
from flask import Blueprint, request
from functions.tasks import Class, pullSources


tasks = Blueprint('tasks', __name__)

@tasks.route('/', methods=['POST'])
def user_index():
    canvaskey = request.form['canvaskey']
    todoistkey = request.form['todoistkey']
    a = Class()
    result = pullSources(canvaskey, todoistkey)
    print(result)