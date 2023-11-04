from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Dict
import database 
import schema
import crud
from API import *

engine, SessionLocal = database.create_Db()
Base = declarative_base()
Base.metadata.create_all(bind=engine)

app = FastAPI()

new_project_name = ''

 # Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/signup/")
async def create_user_route(details : schema.UserCreate, db:Session=Depends(get_db)):
    new_user = crud.create_user(db, dict(details))
    db.close()
    return new_user

@app.get("/login/")
async def login(details : schema.login, db:Session=Depends(get_db)):
    user = crud.get_user_by_email(db, dict(details))
    db.close()
    if user is None:
        raise HTTPException(status_code = 400, detail = "Invalid credentials")

    # Check plaintext password
    if user.password != details.get('password'):
        raise HTTPException(status_code = 400, detail = "Invalid credentials")
    
    global email,id
    email = user.email
    id = user.UserId
    return {"message": "Login successful", "user_id": user.user_id}

@app.post("/create_new_project/")
async def create_new_project(project: schema.ProjectCreateRequest, db:Session = Depends(get_db)):
    try:
        project = crud.create_project(db,dict(project))
        global new_project_name
        new_project_name = project.ProjectName
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Project with this name already exists")

    
@app.post("/Basic_Chat")
async def response(chat_request: schema.ChatSchema, db: Session = Depends(get_db)):
    obj = API()
    chat_content = str(obj.Basic_chat())

    # Create a new ChatSchema object with the updated content
    chat_response = schema.ChatSchema(
        Content = chat_content,
        ProjectName = new_project_name ,
        role = 'Assistant',
        Type = 'Basic' 
        #CreatedDate=datetime.date
    )

    # Pass the new ChatSchema object to the create_chat function
    created_chat = crud.create_chat(db,dict(chat_response))

    return created_chat.Content