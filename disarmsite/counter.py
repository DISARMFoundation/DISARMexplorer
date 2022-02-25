from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import pandas as pd

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Counter
from disarmsite.models import CounterTechnique
from disarmsite.models import Technique
from disarmsite.models import Tactic
from disarmsite.models import Phase


bp = Blueprint('counter', __name__, url_prefix='/counter')

def get_counter(id, check_author=True):
    counter = Counter.query.filter(Counter.id == id).first()
    if counter is None:
        abort(404, f"Counter id {id} doesn't exist.")
    techniques = Technique.query.join(CounterTechnique).filter(CounterTechnique.counter_id == counter.disarm_id)
    return (counter, techniques)

def create_counter_grid():
    counters = Counter.query.join(Tactic).order_by("disarm_id")
    tactics = Tactic.query.join(Phase).order_by("disarm_id")

    # Create grid for clickable visualisation
    df = pd.read_sql(counters.statement, counters.session.bind)
    dflists = df.groupby('tactic_id')['disarm_id'].apply(list).reset_index()
    dfidgrid = pd.DataFrame(dflists['disarm_id'].to_list())
    dfgrid = pd.concat([dflists[['tactic_id']], dfidgrid], axis=1).fillna('')
    counters_grid = [dfgrid[col].to_list() for col in dfgrid.columns]

    # Create dict for use in visualisation and list updates
    df.index = df.disarm_id
    object_names = df[['name']].transpose().to_dict('records')[0]

    # Create dict containing object URLs
    def get_counter_url(tid):
        return url_for('counter.view', id=tid)
    df['url'] = df['id'].apply(get_counter_url)
    object_urls = df[['url']].transpose().to_dict('records')[0]

    # Add tactics ids
    dftactics = pd.read_sql(tactics.statement, counters.session.bind)
    dftactics.index = dftactics.disarm_id
    tactic_names = dftactics[['name']].transpose().to_dict('records')[0]
    object_names.update(tactic_names)

    def get_tactic_url(tid):
        return url_for('tactic.view', id=tid)
    dftactics['url'] = dftactics['id'].apply(get_tactic_url)
    tactic_urls = dftactics[['url']].transpose().to_dict('records')[0]
    object_urls.update(tactic_urls)


    return counters, counters_grid, object_names, object_urls


@bp.route('/')
def index():
    counters, countgrid, countnames = create_counter_grid()
    return render_template('counter/index.html', counters=counters, 
        gridparams=["#bluegrid", '#4641D6', countgrid, countnames])


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    counter, techniques = get_counter(id)
    return render_template('counter/view.html', counter=counter, techniques=techniques)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        disarm_id = request.form['disarm_id']
        name = request.form['name']
        summary = request.form['summary']
        tactic_id = request.form['tactic_id']
        metatechnique_id = request.form['metatechnique_id']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            counter = Counter(disarm_id, metatechnique_id, tactic_id, name, summary)
            db_session.add(counter)
            db_session.commit()
            return redirect(url_for('counter.index'))

    return render_template('counter/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    counter, techniques = get_counter(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            counter.name = name
            counter.summary = summary
            db_session.add(counter)
            db_session.commit()
            return redirect(url_for('counter.index'))

    return render_template('counter/update.html', counter=counter)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    counter, techniques = get_counter(id)
    db_session.delete(counter)
    db_session.commit()
    return redirect(url_for('counter.index'))

