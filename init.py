from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Dict
import json
import datetime
import database 
import schema
import crud
import systemPrompts
from API import *

engine, SessionLocal = database.create_Db()
Base = declarative_base()
Base.metadata.create_all(bind=engine)

app = FastAPI()

global_project_name = ''

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
    systemPrompt = systemPrompts.getBasicSystemPrompt()
    systemPrompt_json = dict({"role" : "system", "content" : systemPrompt})
    try:
        project.UserId = id
        project = crud.create_project(db,dict(project))
        global global_project_name
        global_project_name = project.ProjectName
        created_date = datetime.datetime.now()
        systemPrompt_chat = schema.ChatSchema(
            Content = "system : " + systemPrompt,
            JSON = systemPrompt_json,
            ProjectName = global_project_name,
            role = "system",
            Type = "Basic",
            UserId = id,
            CreatedDate = created_date
        )
        crud.create_chat(db, dict(systemPrompt_chat))
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Project with this name already exists")
    
@app.post("/showExistingProjects")
async def existingProject(db:Session = Depends(get_db)):
    data = {"UserId" : id}
    userProjects = crud.get_projects_by_UserId(db, dict(data))
    return userProjects

@app.post("/continueExistingProject")
async def continueExistingProject(project: schema.ExistingProject, db:Session = Depends(get_db)):
    global global_project_name
    global_project_name = project.ProjectName
    if crud.get_project_by_name(db, dict({"ProjectName" : global_project_name})):
        return global_project_name
    else:
        raise HTTPException(status_code=400, detail="Project with this name does not exists")


@app.post("/BasicContextChat")
async def response(prompt: schema.ChatSchema, db: Session = Depends(get_db)):

    prompt_json = {"role" : "user", "content" : prompt.Content}
    created_date = datetime.datetime.now()
    prompt_chat_obj = schema.ChatSchema(
        Content = "user : " + prompt.Content,
        ProjectName = global_project_name,
        JSON = prompt_json,
        role = "user",
        Type = "Basic",
        UserId = id,
        CreatedDate = created_date
    )
    
    crud.create_chat(db, dict(prompt_chat_obj))

    data = {"ProjectName" : global_project_name, "UserId" : id}
    chats = crud.get_chat_by_ProjectName_and_UserId(db, dict(data))
    chats_array = []
    for i in chats:
        chats_array.append(i.JSON)
    
    print("\n",chats_array,"\n")
    obj = API()
    chat_content = str(obj.contextChat(chats_array))
    response_json = {"role":"assistant", "content": chat_content }

    #Create a new ChatSchema object with the updated content
    created_date = datetime.datetime.now()
    chat_response = schema.ChatSchema(
        Content = "ChatGPT : "+ chat_content,
        ProjectName = global_project_name,
        JSON = response_json,
        role = 'assistant',
        Type = 'Basic' ,
        UserId = id,
        CreatedDate=created_date
    )

    # Pass the new ChatSchema object to the create_chat function
    crud.create_chat(db,dict(chat_response))

    return chat_content

@app.post("/BasicJSONMaker")
async def basicJSONMaker(db: Session = Depends(get_db)):
    data = {"ProjectName" : global_project_name, "UserId" : id}
    chats = crud.get_chat_by_ProjectName_and_UserId(db, dict(data))
    chats_array = []
    for i in chats:
        chats_array.append(i.Content)
    
    obj = API()
    json = str(obj.basicJSONMaker(chats_array))
    update_proj_obj = {"ProjectName" : global_project_name, "BasicInfo" : json, "Details" : ""}
    crud.update_project(db, dict(update_proj_obj))
    return json

