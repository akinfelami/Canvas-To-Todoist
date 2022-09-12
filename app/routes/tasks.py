
from flask import Blueprint, request, render_template, redirect, session, flash, json
from functions.tasks import Class, pullSources, assignments
import time



tasks = Blueprint('tasks', __name__)


@tasks.route('/success')
def succcess():
    return render_template('success.html')

@tasks.route('/failure')
def faliure():
    return render_template('failure.html')

@tasks.route('/', methods=['POST', 'GET'])
def user_index():
    if request.method == 'GET':
        return redirect('/')
    else:
        if not request.form['canvaskey'] and not request.form['todoistkey']:
            return redirect('/')
        course_names = []
        canvaskey = request.form['canvaskey']
        todoistkey = request.form['todoistkey']
        session['canvaskey'] = canvaskey
        session['todoistkey'] = todoistkey
        result = pullSources(canvaskey, todoistkey)
        for course in result:
            course_name = course.get('name')
            course_id = course.get('id')
            if course_name and course_id:
                course_names.append([course_id, course_name.replace('(', '').replace(')', '')])
        
        session['courselist'] = course_names

        return render_template('task.html', courses = course_names)

@tasks.route('/sync', methods=['POST'])
def sync_tasks():
    course_ids = []
    result = None
    canvaskey = session.get('canvaskey', None)
    todoistkey = session.get('todoistkey', None)
    
    for key in request.form:
        course_ids.append(key)

    if len(course_ids)==0:
        return redirect('/')
    try:
        result = assignments(canvaskey, todoistkey, course_ids)
    except Exception as e:
        print(e)
    if result:
        return redirect('/tasks/success')

    return redirect('/tasks/failure')