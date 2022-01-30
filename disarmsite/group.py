from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Group


bp = Blueprint('group', __name__, url_prefix='/group')

def get_group(id, check_author=True):
    group = Group.query.filter(Group.id == id).first()
    if group is None:
        abort(404, f"Group id {id} doesn't exist.")
    return group


@bp.route('/')
def index():
    groups = Group.query.all() #.order_by("disarm_id")
    return render_template('group/index.html', groups=groups)


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    group= get_group(id)
    return render_template('group/view.html', group=group)


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
            group = Group(disarm_id, name, summary)
            db_session.add(group)
            db_session.commit()
            return redirect(url_for('group.index'))

    return render_template('group/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    group = get_group(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            group.name = name
            group.summary = summary
            db_session.add(group)
            db_session.commit()            
            return redirect(url_for('group.index'))

    return render_template('group/update.html', group=group)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    group = get_group(id)
    db_session.delete(group)
    db_session.commit()            
    return redirect(url_for('group.index'))

