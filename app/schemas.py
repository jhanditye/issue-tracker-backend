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
        # would need this blcok here if you were using an ORM where the response comes back as a model and not a tuple which is listable
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
    published: bool = True 

class IssueCreate(IssueBase):
    pass

# Handles direction of us sending data to user
 
class Issue(IssueBase):
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        # would need this blcok here if you were using an ORM where the response comes back as a model and not a tuple which is listable
        orm_mode = True


