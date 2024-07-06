from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:playrakion123@localhost/fastapi'
#'postgresql://<username>:<password>@<ip address/hostname>/<database name>'

engine=create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit = False,autoflush=False, bind=engine)  #this creates a factory function which create DB session 
#for transactions. used for sending SQL queries.SessionLocal is a factory function

Base = declarative_base()

def get_db():
    db=SessionLocal()  # factory function provides db session for each request
    try:
        yield db
    finally:
        db.close() # once context is exited the session is closed