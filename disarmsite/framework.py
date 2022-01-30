from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Framework


bp = Blueprint('framework', __name__, url_prefix='/framework')

def get_framework(id, check_author=True):
    framework = Framework.query.filter(Framework.id == id).first()
    if framework is None:
        abort(404, f"Framework id {id} doesn't exist.")
    return framework


@bp.route('/')
def index():
    frameworks = Framework.query.order_by("disarm_id")
    return render_template('framework/index.html', frameworks=frameworks)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        disarm_id = request.form['disarm_id']
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            framework = Framework(disarm_id, name, summary)
            db_session.add(framework)
            db_session.commit()
            return redirect(url_for('framework.index'))

    return render_template('framework/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    framework = get_framework(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            framework.name = name
            framework.summary = summary
            db_session.add(framework)
            db_session.commit()            
            return redirect(url_for('framework.index'))

    return render_template('framework/update.html', framework=framework)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    framework = get_framework(id)
    db_session.delete(framework)
    db_session.commit()            
    return redirect(url_for('framework.index'))

