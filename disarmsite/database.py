from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os


#engine = create_engine('sqlite:////Users/sara/Dropbox/SJT_Projects_current/DISARM/CODE_AND_DATA/disarmsite/instance/disarmsite.sqlite')
#engine = create_engine('postgresql://sara:@localhost:5432/disarmsite')
engine = create_engine(os.environ['DATABASE_URL2'])

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import disarmsite.models
    Base.metadata.create_all(bind=engine)
