from flask import request, make_response, redirect, render_template, session, url_for, flash
import unittest
from app import create_app
from app.forms import TaskForm, DeleteTaskForm, UpdateTaskForm
from flask_login import login_required, current_user
from app.firestore_service import get_users, get_tasks, put_task, delete_task, update_task


app = create_app()

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response

@app.route('/hello', methods=['GET','POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    task_form = TaskForm()
    delete_form = DeleteTaskForm()
    update_form = UpdateTaskForm()
    context = {
        'user_ip': user_ip,
        'tasks': get_tasks(user_id=username),
        'username': username,
        'task_form': task_form,
        'delete_form': delete_form,
        'update_form': update_form
    }
    if task_form.validate_on_submit():
        put_task(user_id=username, description=task_form.description.data)
        flash('¡Your task was created successfully!')
        return redirect(url_for('hello'))

    return render_template('hello.html', **context)

@app.route('/tasks/delete/<task_id>', methods= ['POST'])
def delete(task_id):
    user_id = current_user.id 
    delete_task(user_id=user_id, task_id=task_id)
    return redirect(url_for('hello'))

@app.route('/tasks/update/<task_id>/<int:done>', methods= ['POST'])
def update(task_id, done):
    user_id = current_user.id 
    update_task(user_id=user_id, task_id=task_id, done=done)

    return redirect(url_for('hello'))