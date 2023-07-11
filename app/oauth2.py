from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from .database import cursor,conn

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


from app import database, schemas
#SECRET KEY
#ALgorithm
#EXPIration TIME

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_expection):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        id = payload.get("user_id")

        if id is None:
            raise credentials_expection
        token_data = schemas.TokenData(id=id)
        return token_data
    except JWTError:
        raise credentials_expection

async def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):

    '''it does both token verifictaion eveyrtime an http request is called and user auth, decidign what acess the user has.
    so in essence : Decode the received token, verify it, and return the current user.

    If the token is invalid, return an HTTP error right away.'''

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)

    cursor.execute("""SELECT * FROM users WHERE id = %s""", (str(token_data.id),))
    user = cursor.fetchone()
    return user
