from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

_engine = create_engine("sqlite:///database.sqlite") 
gunther_sessionmaker = sessionmaker()
gunther_sessionmaker.configure(bind=_engine)

class Model(DeclarativeBase):
    pass

def migrate_up():
    pass

def migrate_down():
    pass

def migrate_fresh():
    pass
