from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import pandas as pd

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Technique
from disarmsite.models import Example
from disarmsite.models import Tactic
from disarmsite.models import Phase
from disarmsite.models import Counter
from disarmsite.models import CounterTechnique
from disarmsite.models import Detection
from disarmsite.models import DetectionTechnique
from disarmsite.models import IncidentTechnique


bp = Blueprint('technique', __name__, url_prefix='/technique')

def get_technique(id, check_author=True):
    technique = Technique.query.join(Tactic).filter(Technique.id == id).first()
    if technique is None:
        abort(404, f"Technique id {id} doesn't exist.")
    examples = Example.query.filter(Example.object_id == technique.disarm_id).order_by("disarm_id")
    counters = Counter.query.join(CounterTechnique).filter(CounterTechnique.technique_id == technique.disarm_id).order_by("disarm_id")
    detections = Detection.query.join(DetectionTechnique).filter(DetectionTechnique.technique_id == technique.disarm_id).order_by("disarm_id")
    incidents = IncidentTechnique.query.filter(IncidentTechnique.technique_id == technique.disarm_id).order_by("incident_id")
    return (technique, examples, counters, detections, incidents)


def create_technique_grid():
    techniques = Technique.query.join(Tactic).order_by("disarm_id")
    print('{}'.format(techniques))
    tactics = Tactic.query.join(Phase).order_by("disarm_id")
    print('tactics: {}'.format(tactics))

    # Create grid for clickable visualisation
    df = pd.read_sql(techniques.statement, techniques.session.bind)
    dflists = df.groupby('tactic_id')['disarm_id'].apply(list).reset_index()
    dfidgrid = pd.DataFrame(dflists['disarm_id'].to_list())
    dfgrid = pd.concat([dflists[['tactic_id']], dfidgrid], axis=1).fillna('')
    techniques_grid = [dfgrid[col].to_list() for col in dfgrid.columns]

    # Create dict for use in visualisation and list updates
    df.index = df.disarm_id
    object_names = df[['name']].transpose().to_dict('records')[0]

    # Create dict containing object URLs
    def get_technique_url(tid):
        return url_for('technique.view', id=tid)
    df['url'] = df['id'].apply(get_technique_url)
    object_urls = df[['url']].transpose().to_dict('records')[0]

    # Add tactics ids
    dftactics = pd.read_sql(tactics.statement, techniques.session.bind)
    dftactics.index = dftactics.disarm_id
    tactic_names = dftactics[['name']].transpose().to_dict('records')[0]
    object_names.update(tactic_names)

    def get_tactic_url(tid):
        return url_for('tactic.view', id=tid)
    dftactics['url'] = dftactics['id'].apply(get_tactic_url)
    tactic_urls = dftactics[['url']].transpose().to_dict('records')[0]
    object_urls.update(tactic_urls)

    return techniques, techniques_grid, object_names, object_urls


@bp.route('/')
def index():
    techniques, techgrid, technames, techurls = create_technique_grid()

    return render_template('technique/index.html', techniques=techniques, 
        gridparams=["#redgrid", '#E74C3C', techgrid, technames])



@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    technique, examples, counters, detections, incidents = get_technique(id)
    return render_template('technique/view.html', technique=technique, examples=examples, counters=counters, 
        detections=detections, incidents=incidents)


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
            technique = Technique(disarm_id, tactic_id, name, summary)
            db_session.add(technique)
            db_session.commit()
            return redirect(url_for('technique.index'))

    return render_template('technique/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    technique, examples, counters, detections, incidents = get_technique(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            technique.name = name
            technique.summary = summary
            db_session.add(technique)
            db_session.commit()
            return redirect(url_for('technique.index'))

    return render_template('technique/update.html', technique=technique)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    technique, examples, counters, detections, incidents = get_technique(id)
    db_session.delete(technique)
    db_session.commit()
    return redirect(url_for('technique.index'))

