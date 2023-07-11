from fastapi import FastAPI

from fastapi import Depends, FastAPI, Response,status,HTTPException
from app import models, schemas,utils
from .database import get_db, engine
from .routers import issue, user,auth



app = FastAPI()

@app.get("/")
def hello_world():
    return {"hello":"lit"}



app.include_router(auth.router)
app.include_router(user.router)
#app.include_router(issue.router)