from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Task
from disarmsite.models import Tactic

bp = Blueprint('task', __name__, url_prefix='/task')

def get_task(id, check_author=True):
    task = Task.query.join(Tactic).filter(Task.id == id).first()
    if task is None:
        abort(404, f"Task id {id} doesn't exist.")
    return task


@bp.route('/')
def index():
    tasks = Task.query.join(Tactic).order_by("disarm_id")
    return render_template('task/index.html', tasks=tasks)


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    task = get_task(id)
    return render_template('task/view.html', task=task)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        disarm_id = request.form['disarm_id']
        name = request.form['name']
        summary = request.form['summary']
        tactic_id = request.form['tactic_id']
        framework_id = request.form['framework_id']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            task = Task(disarm_id, tactic_id, framework_id, name, summary)
            db_session.add(task)
            db_session.commit()
            return redirect(url_for('task.index'))

    return render_template('task/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    task = get_task(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            task.name = name
            task.summary = summary
            db_session.add(task)
            db_session.commit()
            return redirect(url_for('task.index'))

    return render_template('task/update.html', task=task)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    task = get_task(id)
    db_session.delete(task)
    db_session.commit()
    return redirect(url_for('task.index'))

