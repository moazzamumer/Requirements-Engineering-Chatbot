from sqlalchemy.orm import Session
from models import User, Project, Chat
import database

_, SessionLocal = database.create_Db()


# User Functions
def create_user(db: Session, data: dict):
    user = User(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db: Session, data: dict):
    user_id = data.get('UserId')
    return db.query(User).filter(User.UserId == user_id).first()

def get_user_by_email(db: Session, data: dict):
    email = data.get('email')
    return db.query(User).filter(User.email == email).first()

def update_user(db: Session, user: User, data: dict):
    user.username = data.get('username', user.username)
    user.password = data.get('password', user.password)
    user.email = data.get('email', user.email)
    db.commit()
    return user

def delete_user(db: Session, data: dict):
    user_id = data.get('UserId')
    user = db.query(User).filter(User.UserId == user_id).first()
    if user:
        db.delete(user)
        db.commit()


# Project Table Functions
def create_project(db: Session, data: dict):
    project = Project(**data)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

def get_project_by_name(db: Session, data: dict):
    project_name = data.get('ProjectName')
    return db.query(Project).filter(Project.ProjectName == project_name).first()

def update_project(db: Session, data: dict):
    project_name = data.get('ProjectName')
    project = db.query(Project).filter(Project.ProjectName == project_name).first()
    if project:
        project.BasicInfo = data.get('BasicInfo', project.BasicInfo)
        project.Details = data.get('Details', project.Details)
        db.commit()
        return project
    
def delete_project(db: Session, data: dict):
    project_name = data.get('ProjectName')
    project = db.query(Project).filter(Project.ProjectName == project_name).first()
    if project:
        db.delete(project)
        db.commit()


# Chat Table Functions
def create_chat(db: Session, data: dict):
    chat = Chat(**data)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def get_chat_by_project_name(db: Session, data: dict):
    project_name = data.get('ProjectName')
    return db.query(Chat).filter(Chat.ProjectName == project_name).all()

def update_chat(db: Session, data: dict):
    content = data.get('Content')
    project_name = data.get('ProjectName')
    chat = db.query(Chat).filter(Chat.Content == content, Chat.ProjectName == project_name).first()
    if chat:
        chat.JSON = data.get('JSON', chat.JSON)
        chat.role = data.get('role', chat.role)
        chat.Type = data.get('Type', chat.Type)
        db.commit()
        return chat

def delete_chat(db: Session, data: dict):
    content = data.get('Content')
    project_name = data.get('ProjectName')
    chat = db.query(Chat).filter(Chat.Content == content, Chat.ProjectName == project_name).first()
    if chat:
        db.delete(chat)
        db.commit()