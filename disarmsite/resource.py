from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Resource


bp = Blueprint('resource', __name__, url_prefix='/resource')

def get_resource(id, check_author=True):
    resource = Resource.query.filter(Resource.id == id).first()
    if resource is None:
        abort(404, f"Resource id {id} doesn't exist.")
    return resource


@bp.route('/')
def index():
    resources = Resource.query.all() #.order_by("disarm_id")
    return render_template('resource/index.html', resources=resources)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        disarm_id = request.form['disarm_id']
        name = request.form['name']
        summary = request.form['summary']
        resource_type = request.form['resource_type']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            resource = Resource(disarm_id, name, summary, resource_type)
            db_session.add(resource)
            db_session.commit()
            return redirect(url_for('resource.index'))

    return render_template('resource/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    resource = get_resource(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            resource.name = name
            resource.summary = summary
            db_session.add(resource)
            db_session.commit()            
            return redirect(url_for('resource.index'))

    return render_template('resource/update.html', resource=resource)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    resource = get_resource(id)
    db_session.delete(resource)
    db_session.commit()            
    return redirect(url_for('resource.index'))

