from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Tactic
from disarmsite.models import Phase


bp = Blueprint('tactic', __name__, url_prefix='/tactic')


def get_tactic(id, check_author=True):
    tactic = Tactic.query.join(Phase).filter(Tactic.id == id )
    if tactic is None:
        abort(404, f"Tactic id {id} doesn't exist.")
    return tactic


@bp.route('/')
def index():
    tactics = Tactic.query.join(Phase).order_by("disarm_id")
    return render_template('tactic/index.html', tactics=tactics)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        disarm_id = request.form['disarm_id']
        name = request.form['name']
        summary = request.form['summary']
        rank = request.form['rank']
        phase_id = request.form['phase_id']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            tactic = Tactic(disarm_id, phase_id, rank, name, summary)
            db_session.add(counter)
            db_session.commit()
            return redirect(url_for('tactic.index'))

    return render_template('tactic/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    tactic = get_tactic(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            tactic.name = name
            tactic.summary = summary
            db_session.add(tactic)
            db_session.commit()
            return redirect(url_for('tactic.index'))

    return render_template('tactic/update.html', tactic=tactic)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    tactic = get_tactic(id)
    db_session.delete(tactic)
    db_session.commit()
    return redirect(url_for('tactic.index'))

