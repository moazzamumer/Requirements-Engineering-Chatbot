from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Dict
import datetime
import database 
import schema
import crud
import models
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

@app.post("/login")
async def login(details : schema.login, db:Session=Depends(get_db)):
    user = crud.get_user_by_email(db, dict(details))
    db.close()
    if user is None:
        raise HTTPException(status_code = 400, detail = "Invalid credentials")

    # Check plaintext password
    if user.password != details.password:
        raise HTTPException(status_code = 400, detail = "Invalid credentials")
    
    global email,id
    email = user.email
    id = user.UserId
    return {"message": "Login successful", "user_id": user.UserId}

@app.post("/create_new_project/")
async def create_new_project(project: schema.ProjectCreateRequest, db:Session = Depends(get_db)):
    try:
        project = crud.create_project(db,dict(project))
        global new_project_name
        new_project_name = project.ProjectName
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Project with this name already exists")
    

    
@app.post("/BasicContextChat")
async def response(prompt: schema.ChatSchema, db: Session = Depends(get_db)):

    prompt_json = f"{{'role' : 'user', 'content' : '{prompt.Content}'}}"
    created_date = datetime.datetime.now()
    prompt_chat_obj = schema.ChatSchema(
        Content = prompt.Content,
        ProjectName = new_project_name,
        JSON = prompt_json,
        role = "User",
        Type = "Basic",
        CreatedDate = created_date
    )
    
    # prompt_chat_obj = models.Chat(
    #     Content = prompt.Content,
    #     ProjectName = new_project_name,
    #     JSON = prompt_json,
    #     role = "User",
    #     Type = "Basic",
    #     CreatedDate = datetime.date
    # )
    crud.create_chat(db, dict(prompt_chat_obj))

    data = {"ProjectName":new_project_name, "UserEmail" : email}
    chat_array = []
    for json in crud.get_chatJSON_by_ProjectName_and_UserEmail(db, data):
        if json:
            chat_array.append(json)

    chat_array_json = "[" + ",".join(chat_array) + "]"
    print("\n",chat_array_json,"\n")
    obj = API()
    chat_content = str(obj.contextChat(chat_array_json))
    response_json = f"{{'role':'assistant', 'content':'{chat_content}'}}"

    #Create a new ChatSchema object with the updated content
    created_date = datetime.datetime.now()
    chat_response = schema.ChatSchema(
        Content = chat_content,
        ProjectName = new_project_name,
        JSON = response_json,
        role = 'Assistant',
        Type = 'Basic' ,
        CreatedDate=created_date
    )

    # chat_response = models.Chat(
    #     Content = chat_content,
    #     ProjectName = new_project_name ,
    #     JSON = response_json,
    #     role = 'Assistant',
    #     Type = 'Basic' ,
    #     CreatedDate=datetime.date
    # )

    # Pass the new ChatSchema object to the create_chat function
    crud.create_chat(db,dict(chat_response))

    return chat_content