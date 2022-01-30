from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Phase


bp = Blueprint('phase', __name__, url_prefix='/phase')

def get_phase(id, check_author=True):
    phase = Phase.query.filter(Phase.id == id).first()
    if phase is None:
        abort(404, f"Phase id {id} doesn't exist.")
    return phase


@bp.route('/')
def index():
    phases = Phase.query.all() #.order_by("disarm_id")
    return render_template('phase/index.html', phases=phases)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        disarm_id = request.form['disarm_id']
        name = request.form['name']
        summary = request.form['summary']
        rank = request.form['rank']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            phase = Phase(disarm_id, rank, name, summary)
            db_session.add(phase)
            db_session.commit()
            return redirect(url_for('phase.index'))

    return render_template('phase/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    phase = get_phase(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            phase.name = name
            phase.summary = summary
            db_session.add(phase)
            db_session.commit()            
            return redirect(url_for('phase.index'))

    return render_template('phase/update.html', phase=phase)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    phase = get_phase(id)
    db_session.delete(phase)
    db_session.commit()            
    return redirect(url_for('phase.index'))

