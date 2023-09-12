from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email:EmailStr
    created_at: datetime 

    class Config:
        orm_mode = True

# Login

class UserLogin(BaseModel):
    email: EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str] = None


# Projects 
class ProjectCreate(BaseModel):
    name: str
    description: str

class ProjectOut(BaseModel):
    id: int
    name: str
    description: str 

    class Config:
        orm_mode = True

class UserProjectAssociation(BaseModel):
    user_id: int
    project_id: int

    class Config:
        orm_mode = True


# Handles direction of user sending data to us 
class IssueBase(BaseModel):
    title: str
    content: str

class IssueCreate(IssueBase):
    pass

# Handles direction of us sending data to user
class Issue(IssueBase):
    id:int
    created_at: datetime
    assigned_user_id: int
    assigned_user: UserOut
    project_id: int
    project: ProjectOut

    class Config:
        orm_mode = True


class IssueAssignment(BaseModel):
    user_id: int