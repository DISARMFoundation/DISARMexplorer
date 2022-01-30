from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from disarmsite.auth import login_required
from disarmsite.database import db_session
from disarmsite.models import Tool


bp = Blueprint('tool', __name__, url_prefix='/tool')

def get_tool(id, check_author=True):
    tool = Tool.query.filter(Tool.id == id).first()
    if tool is None:
        abort(404, f"Tool id {id} doesn't exist.")
    return tool


@bp.route('/')
def index():
    tools = Tool.query.all() #.order_by("disarm_id")
    return render_template('tool/index.html', tools=tools)


@bp.route('/<int:id>/view', methods=('GET', 'POST'))
def view(id):
    tool = get_tool(id)
    return render_template('tool/view.html', tool=tool)


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
            tool = Tool(disarm_id, name, summary)
            db_session.add(tool)
            db_session.commit()
            return redirect(url_for('tool.index'))

    return render_template('tool/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    tool = get_tool(id)

    if request.method == 'POST':
        name = request.form['name']
        summary = request.form['summary']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            tool.name = name
            tool.summary = summary
            db_session.add(tool)
            db_session.commit()            
            return redirect(url_for('tool.index'))

    return render_template('tool/update.html', tool=tool)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    tool = get_tool(id)
    db_session.delete(tool)
    db_session.commit()            
    return redirect(url_for('tool.index'))

