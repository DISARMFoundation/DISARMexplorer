from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Externalgroup


bp = Blueprint('externalgroup', __name__, url_prefix='/externalgroup')

def get_externalgroup(id, check_author=True):
    externalgroup = Externalgroup.query.filter(Externalgroup.id == id).first()
    if externalgroup is None:
        abort(404, f"Externalgroup id {id} doesn't exist.")
    return externalgroup


@bp.route('/')
def index():
    externalgroups = Externalgroup.query.all() #.order_by("disarm_id")
    return render_template('externalgroup/index.html', externalgroups=externalgroups)


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    externalgroup= get_externalgroup(id)
    return render_template('externalgroup/view.html', externalgroup=externalgroup)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        disarm_id = request.form['disarm_id']
        name = request.form['name']
        summary = request.form['summary']
        #FIXIT add other variables
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            externalgroup = Externalgroup(disarm_id, name, summary)
            db_session.add(externalgroup)
            db_session.commit()
            return redirect(url_for('externalgroup.index'))

    return render_template('externalgroup/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    externalgroup = get_externalgroup(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            externalgroup.name = name
            externalgroup.summary = summary
            db_session.add(externalgroup)
            db_session.commit()            
            return redirect(url_for('externalgroup.index'))

    return render_template('externalgroup/update.html', externalgroup=externalgroup)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    externalgroup = get_externalgroup(id)
    db_session.delete(externalgroup)
    db_session.commit()            
    return redirect(url_for('externalgroup.index'))

