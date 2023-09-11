from typing import List, Optional 
from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.params import Body
from app import models, oauth2, schemas
from ..database import get_db
from sqlalchemy.orm import Session

# Routes for Projects
router = APIRouter(
    prefix="/projects",
    tags=['Projects']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProjectOut)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db)
):
    new_project = models.Project(**project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.post("/{project_id}/join", status_code=status.HTTP_200_OK, response_model=schemas.UserProjectAssociation)
def join_project(
    project_id: int,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    existing_association = db.query(models.user_project_association_table).filter(
        models.user_project_association_table.c.user_id == current_user['id'],
        models.user_project_association_table.c.project_id == project_id
    ).first()

    if existing_association:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User is already part of this project.")

    association_data = {"user_id": current_user['id'], "project_id": project_id}
    db.execute(models.user_project_association_table.insert().values(**association_data))
    db.commit()
    # As you're returning an association in the response, 
    # I'm returning the association_data here. 
    # You might need to adjust the response model or the returned data 
    # to make sure it aligns with your `schemas.UserProjectAssociation`.
    return association_data

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ProjectOut])
def list_projects(
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    # Using the association table, retrieve the projects for a user.
    projects = db.query(models.Project).join(
        models.user_project_association_table
    ).filter(
        models.user_project_association_table.c.user_id == current_user['id']
    )

    return projects.all()
