from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Incident
from disarmsite.models import IncidentTechnique


bp = Blueprint('incident', __name__, url_prefix='/incident')

# FIXIT: add a routine get_incident_minimal that only gets basic incident data, not cross-table stuff

def get_incident(id, check_author=True):
    incident = Incident.query.filter(Incident.id == id).first()
    if incident is None:
        abort(404, f"Incident id {id} doesn't exist.")
    techniques = IncidentTechnique.query.filter(IncidentTechnique.incident_id == incident.disarm_id).order_by("technique_id")
    return incident, techniques


@bp.route('/')
def index():
    incidents = Incident.query.all() #.order_by("disarm_id")
    return render_template('incident/index.html', incidents=incidents)


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    incident, techniques = get_incident(id)
    return render_template('incident/view.html', incident=incident, techniques=techniques)


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
            incident = Incident(disarm_id, name, summary)
            db_session.add(incident)
            db_session.commit()
            return redirect(url_for('incident.index'))

    return render_template('incident/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    incident, techniques = get_incident(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            incident.name = name
            incident.summary = summary
            db_session.add(incident)
            db_session.commit()            
            return redirect(url_for('incident.index'))

    return render_template('incident/update.html', incident=incident)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    incident, techniques = get_incident(id)
    db_session.delete(incident)
    db_session.commit()            
    return redirect(url_for('incident.index'))

