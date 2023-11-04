from pydantic import BaseModel
from pydantic import EmailStr

class UserBase(BaseModel):
    pass

class UserCreate(BaseModel):
    password: str
    email:str
    username:str

class login(BaseModel):
    email:str
    password:str