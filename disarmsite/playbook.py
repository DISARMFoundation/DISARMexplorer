from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Playbook


bp = Blueprint('playbook', __name__, url_prefix='/playbook')

def get_playbook(id, check_author=True):
    playbook = Playbook.query.filter(Playbook.id == id).first()
    if playbook is None:
        abort(404, f"Playbook id {id} doesn't exist.")
    return playbook


@bp.route('/')
def index():
    playbooks = Playbook.query.all() #.order_by("disarm_id")
    return render_template('playbook/index.html', playbooks=playbooks)


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
            playbook = Playbook(disarm_id, object_id, name, summary)
            db_session.add(playbook)
            db_session.commit()
            return redirect(url_for('playbook.index'))

    return render_template('playbook/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    playbook = get_playbook(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            playbook.name = name
            playbook.summary = summary
            db_session.add(playbook)
            db_session.commit()            
            return redirect(url_for('playbook.index'))

    return render_template('playbook/update.html', playbook=playbook)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    playbook = get_playbook(id)
    db_session.delete(playbook)
    db_session.commit()            
    return redirect(url_for('playbook.index'))

