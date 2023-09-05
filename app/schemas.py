from datetime import datetime
from typing import Optional

from pydantic import  BaseModel, EmailStr



class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email:EmailStr
    created_at: datetime 

    class Config:
        # would need this block here if you were using an ORM where the response comes back as a model and not a tuple which is listable
        orm_mode = True


## Login

class UserLogin(BaseModel):
    email: EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str] = None
    

# Handles direction of user sending data to us 

class IssueBase(BaseModel):
    title: str
    content: str

class IssueCreate(IssueBase):
    pass

# Handles direction of us sending data to user
 
class Issue(IssueBase):
    created_at: datetime
    assigned_user_id: int
    assigned_user: UserOut

    class Config:
        # would need this block here if you were using an ORM where the response comes back as a model and not a tuple which is listable
        orm_mode = True


# Teams 

class TeamCreate(BaseModel):
    name: str
    description: str

class TeamOut(BaseModel):
    id: int
    name: str
    description: str 

    class Config:
        # would need this block here if you were using an ORM where the response comes back as a model and not a tuple which is listable
        orm_mode = True


class UserTeamAssociation(BaseModel):
    user_id: int
    team_id: int

    class Config:
        orm_mode = True
