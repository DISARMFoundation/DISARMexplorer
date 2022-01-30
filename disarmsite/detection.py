from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Detection
from disarmsite.models import Technique
from disarmsite.models import DetectionTechnique


bp = Blueprint('detection', __name__, url_prefix='/detection')

def get_detection(id, check_author=True):
    detection = Detection.query.filter(Detection.id == id).first()

    if detection is None:
        abort(404, f"Detection id {id} doesn't exist.")

    techniques = Technique.query.join(DetectionTechnique).filter(DetectionTechnique.detection_id == detection.disarm_id )
    return (detection, techniques)

@bp.route('/')
def index():
    detections = Detection.query.order_by("disarm_id")
    return render_template('detection/index.html', detections=detections)


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    detection, techniques = get_detection(id)
    return render_template('detection/view.html', detection=detection, techniques=techniques)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        disarm_id = request.form['disarm_id']
        tactic_id = request.form['tactic_id']
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            detection = Detection(disarm_id, tactic_id, name, summary)
            db_session.add(detection)
            db_session.commit()
            return redirect(url_for('detection.index'))

    return render_template('detection/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    detection, techniques = get_detection(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            detection.name = name
            detection.summary = summary
            db_session.add(detection)
            db_session.commit()
            return redirect(url_for('detection.index'))

    return render_template('detection/update.html', detection=detection)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    detection, techniques = get_detection(id)
    db_session.delete(detection)
    db_session.commit()
    return redirect(url_for('detection.index'))

