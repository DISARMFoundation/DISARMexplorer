import os


basedir = os.path.abspath(os.path.dirname(__file__))


# Keys
SECRET_KEY = os.environ.get('SECRET_KEY') or 'yeah-whatever-thingy'


# Database setup
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'disarmsite.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = False

