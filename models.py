from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Sequence, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import registry
import database

engine, SessionLocal = database.create_Db()

Base = declarative_base()
mapper_registry = registry()



class User(Base):
    __tablename__ = "users"

    UserId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)

class Project(Base):
    __tablename__ = 'projects'

    ProjectName = Column(String, primary_key=True, index=True)
    BasicInfo = Column(String)
    Details = Column(String)
    UserId = Column(Integer, ForeignKey('users.UserId'))  # Correct foreign key reference
    CreatedDate = Column(DateTime, server_default=func.now())
    #user = relationship("User", back_populates="projects")


class Chat(Base):
    __tablename__ = 'chats'
    # Define an auto-incrementing primary key
    ChatId = Column(Integer, primary_key=True, autoincrement=True)
    Content = Column(String)
    JSON = Column(String)
    ProjectName = Column(String, ForeignKey('projects.ProjectName'))
    role = Column(String)
    Type = Column(String)
    UserEmail = Column(String, ForeignKey('users.email'))
    CreatedDate = Column(DateTime, server_default=func.now())
    #project = relationship("Project", back_populates="chats")


Base.metadata.create_all(bind=engine)