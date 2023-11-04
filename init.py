from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import database
import crud
import s

engine, SessionLocal = database.create_Db()
Base = declarative_base()
Base.metadata.create_all(bind=engine)

app = FastAPI()

 # Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("signup",response_model=s.UserBase)
async def create_user_route(details : s.UserCreate, db:Session=Depends(get_db)):
    new_user = crud.create_user(db, details)
    db.close()
    return new_user

@app.post("/login/")
async def login(details : dict, db:Session=Depends(get_db)):
    user = crud.get_user_by_email(db, details)
    db.close()
    if user is None:
        raise HTTPException(status_code=400, detail = "Invalid credentials")

    # Check plaintext password
    if user.password != details.get('password'):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": user.user_id}