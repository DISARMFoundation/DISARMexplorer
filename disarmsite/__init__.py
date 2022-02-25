import os

from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from disarmsite.database import init_db
from disarmsite.database import db_session
from . import auth
from . import counter
from . import detection
from . import example
from . import framework
from . import externalgroup
from . import incident
from . import metatechnique
from . import phase
from . import playbook
from . import resource
from . import responsetype
from . import tactic
from . import task
from . import technique
from . import tool
import sqlite3


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Configuration settings
    # app.config.from_mapping(
    #     SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev',
    #     DATABASE=os.path.join(app.instance_path, 'disarmsite.sqlite'),
    #     SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'disarmsite.sqlite'),
    # )
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev',
        SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL2'],
    )
    # print('{}'.format(app.config))

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Main route: to index page
    # EDIT: changed top colours from red '#E74C3C' and blue '#4641D6' because they were hard to read. 
    @app.route('/')
    def index():
        (techniques, techgrid, technames, techurls) = technique.create_technique_grid()
        (counters, countergrid, counternames, counterurls) = counter.create_counter_grid()
        return render_template('index.html', 
            redgridparams=["#redgrid", '#F5B7B1', techgrid, technames, techurls, "DISARM Red Framework - incident creator TTPs"],
            bluegridparams=["#bluegrid", '#AED6F1', countergrid, counternames, counterurls, "DISARM Blue Framework - responder TTPs"])


    # About page
    @app.route('/about')
    def about():
        return render_template('about.html')

    # Objects page
    @app.route('/objects')
    def objects():
        return render_template('objects.html')

    # Testing route: a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/textgrid')
    def textgrid():
        (techniques, techgrid, technames, techurls) = technique.create_technique_grid()
        (counters, countergrid, counternames, counterurls) = counter.create_counter_grid()
        return render_template('textgrid.html', 
            redgridparams=["#redgrid", '#E74C3C', techgrid, technames, techurls, "DISARM Red Framework - incident creator TTPs"],
            bluegridparams=["#bluegrid", '#AED6F1', countergrid, counternames, counterurls, "DISARM Blue Framework - responder TTPs"],
            )


    @app.route('/mapblobs')
    def mapblobs():
        array = []
        return render_template('mapblobs.html', array=array)


    # do the database stuff
    init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # register all the object code
    app.register_blueprint(auth.bp)
    app.register_blueprint(counter.bp)
    app.register_blueprint(detection.bp)
    app.register_blueprint(example.bp)
    app.register_blueprint(framework.bp)
    app.register_blueprint(externalgroup.bp)
    app.register_blueprint(incident.bp)
    app.register_blueprint(metatechnique.bp)
    app.register_blueprint(phase.bp)
    app.register_blueprint(playbook.bp)
    app.register_blueprint(resource.bp)
    app.register_blueprint(responsetype.bp)
    app.register_blueprint(tactic.bp)
    app.register_blueprint(task.bp)
    app.register_blueprint(technique.bp)
    app.register_blueprint(tool.bp)
    app.add_url_rule('/', endpoint='index')

    return app
