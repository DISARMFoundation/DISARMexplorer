from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Example


bp = Blueprint('example', __name__, url_prefix='/example')

def get_example(id, check_author=True):
    example = Example.query.filter(Example.id == id).first()
    if example is None:
        abort(404, f"Example id {id} doesn't exist.")
    return example


@bp.route('/')
def index():
    examples = Example.query.all() #.order_by("disarm_id")
    return render_template('example/index.html', examples=examples)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        disarm_id = request.form['disarm_id']
        object_id = request.form['object_id']
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            example = Example(disarm_id, object_id, name, summary)
            db_session.add(example)
            db_session.commit()
            return redirect(url_for('example.index'))

    return render_template('example/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    example = get_example(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            example.name = name
            example.summary = summary
            db_session.add(example)
            db_session.commit()            
            return redirect(url_for('example.index'))

    return render_template('example/update.html', example=example)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    example = get_example(id)
    db_session.delete(example)
    db_session.commit()            
    return redirect(url_for('example.index'))

