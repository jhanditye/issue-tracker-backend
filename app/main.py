from fastapi import FastAPI

from fastapi import Depends, FastAPI, Response,status,HTTPException
#from app import models, schemas,utils
from .routers import issue, project, user,auth

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()



# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # You might want to restrict this to your frontend's origin like "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello_world():
    return {"hello":"world of docker"}

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(issue.router)
app.include_router(project.router)
