from curses import flash
from re import T
from flask import Blueprint, request, render_template, redirect, session, flash
from functions.tasks import Class, pullSources, assignments


tasks = Blueprint('tasks', __name__)

@tasks.route('/', methods=['POST', 'GET'])
def user_index():
    if request.method == 'GET':
        return redirect('/')
    else:
        course_names = []
        canvaskey = request.form['canvaskey']
        todoistkey = request.form['todoistkey']
        session['canvaskey'] = canvaskey
        session['todoistkey'] = todoistkey
        result = pullSources(canvaskey, todoistkey)
        for course in result:
            course_name = course.get('name')
            if course_name:
                course_names.append(course_name.replace('(', '').replace(')', ''))
        

        return render_template('task.html', courses = course_names)

@tasks.route('/sync', methods=['POST'])
def sync_tasks():
    canvaskey = session.get('canvaskey', None)
    todoistkey = session.get('todoistkey', None)
    result = assignments(canvaskey, todoistkey)


    return redirect('/')