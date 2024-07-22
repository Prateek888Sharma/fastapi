from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#Anything that we donont want ot be exposed like passwords, secret keys and anything that needs to be updated based on the
#environment in which it will be running needs to be in envrionment variables.Environment variables are configured on the system and any 
#application running on that system will be able to access those environment variables

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"
                                                                       
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

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='playrakion123',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database Connection Established")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print(error)
#         time.sleep(2)