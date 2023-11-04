from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import EmailStr

class UserBase(BaseModel):
    pass

class UserCreate(BaseModel):
    username:str
    password: str
    email:str
    

class login(BaseModel):
    email:str
    password:str

class ProjectCreateRequest(BaseModel):
    ProjectName: str
    BasicInfo: str
    Details: str
    

class ChatSchema(BaseModel):
    ChatId: Optional[int] = None
    Content: str
    JSON: Optional[str] = None
    ProjectName: str
    role: Optional[str]
    Type: Optional[str] = None
    CreatedDate: Optional[datetime] = None

    class Config:
        from_attributes = True