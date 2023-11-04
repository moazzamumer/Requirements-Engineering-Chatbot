from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_Db():

    DATABASE_URL = "postgresql://moazzam99:moazzam99@localhost/requirementsbot"

    engine = create_engine(DATABASE_URL)

    # Create a session class
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    print("Database Connection Established...")

    return engine, SessionLocal