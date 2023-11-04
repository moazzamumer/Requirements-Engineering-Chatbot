from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def create_Db():

    DATABASE_URL = "postgresql://moazzam99:moazzam99@localhost/requirementsbot"

    #DATABASE_URL = "postgresql://postgres:unity007@localhost:5432/requirementsbot"

    engine = create_engine(DATABASE_URL)

    # Create a session class
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Baase = declarative_base()
    

    print("Database Connection Established...")

    return engine, SessionLocal