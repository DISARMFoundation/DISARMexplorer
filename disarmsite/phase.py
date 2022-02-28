from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Phase
from disarmsite.models import Tactic
from disarmsite.models import Technique
from disarmsite.models import Counter


bp = Blueprint('phase', __name__, url_prefix='/phase')

def get_phase(id, check_author=True):
    phase = Phase.query.filter(Phase.id == id).first()
    if phase is None:
        abort(404, f"Phase id {id} doesn't exist.")

    tactics = Tactic.query.filter(Tactic.phase_id == phase.disarm_id).order_by("disarm_id")

    return (phase, tactics)


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


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    (phase, tactics) = get_phase(id)
    return render_template('phase/view.html', phase=phase, tactics=tactics)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    (phase, tactics) = get_phase(id)

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
    (phase, tactics) = get_phase(id)
    db_session.delete(phase)
    db_session.commit()            
    return redirect(url_for('phase.index'))

