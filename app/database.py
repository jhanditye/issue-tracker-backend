from .config import settings

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
import time
import psycopg2

from app import models
from .config import settings 
'''
while True:
    try:
        # should never be hard-coding these value in here
        conn = psycopg2.connect(host=settings.DATABASE_HOSTNAME,database=settings.DATABASE_NAME ,user=settings.DATABASE_USERNAME ,password=settings.DATABASE_PASSWORD, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database slapt")
        break
    except Exception as error:
        print("You done failed on the database side of things my gut")
        print(str(error))
        time.sleep(2)


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}" # never good to behard coding this 

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
# Create session for when we need to and close it when done, we will pass this into crud operations
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''

Base = declarative_base()
