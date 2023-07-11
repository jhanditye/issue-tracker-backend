
from .. import database, schemas, models, utils,oauth2
from typing import List
from fastapi import Depends,status,HTTPException, APIRouter
from fastapi.params import Body
from app import schemas
from ..database import get_db, engine,cursor,conn
from app.schemas import IssueCreate
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentification'])


@router.post('/login', response_model = schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    #cursor.execute ("""SELECT * from users WHERE email = %s""", (user_credentials.username,))
    #user = cursor.fetchone()
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail = f"Invalid credentials")
    
    matched_password = utils.verify_password(user_credentials.password,user.password)

    if not matched_password:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail = f"Invalid credentials")
    
    #Create token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    #Return token 
    return {"access_token": access_token ,"token_type": "bearer"}