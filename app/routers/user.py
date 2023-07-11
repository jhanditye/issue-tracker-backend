
from fastapi import Depends,status,HTTPException,APIRouter
from fastapi.params import Body
from app import models, schemas
from ..database import get_db,cursor,conn
from app.schemas import UserCreate
from sqlalchemy.orm import Session
from ..utils import get_password_hash

#### Routes for users

router = APIRouter(
    prefix="/users",
    tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
     #hash passwords
    unhashed_password  = user.password
    hashed_password = get_password_hash(unhashed_password)
    user.password = hashed_password


    #cursor.execute("""INSERT INTO users (email,password) VALUES (%s,%s) returning *""", (user.email, user.password))
    #new_user = cursor.fetchone()
    #need to commit change with posts
    #conn.commit()

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user   

