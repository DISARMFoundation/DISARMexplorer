from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Responsetype


bp = Blueprint('responsetype', __name__, url_prefix='/responsetype')

def get_responsetype(id, check_author=True):
    responsetype = Responsetype.query.filter(Responsetype.id == id).first()
    if responsetype is None:
        abort(404, f"Responsetype id {id} doesn't exist.")
    return responsetype


@bp.route('/')
def index():
    responsetypes = Responsetype.query.all() #.order_by("disarm_id")
    return render_template('responsetype/index.html', responsetypes=responsetypes)


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
            responsetype = Responsetype(disarm_id, name, summary)
            db_session.add(responsetype)
            db_session.commit()
            return redirect(url_for('responsetype.index'))

    return render_template('responsetype/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    responsetype = get_responsetype(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            responsetype.name = name
            responsetype.summary = summary
            db_session.add(responsetype)
            db_session.commit()            
            return redirect(url_for('responsetype.index'))

    return render_template('responsetype/update.html', responsetype=responsetype)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    responsetype = get_responsetype(id)
    db_session.delete(responsetype)
    db_session.commit()            
    return redirect(url_for('responsetype.index'))

