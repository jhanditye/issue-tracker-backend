from typing import List, Optional 
from fastapi import Depends, Response, status, HTTPException, APIRouter
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
    project: schemas.ProjectOut,
    db: Session = Depends(get_db)
):
    new_project = models.Project(**project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.put("/{project_id}", status_code=status.HTTP_200_OK, response_model=schemas.ProjectOut)
def update_project(
    project_id: int,
    updated_project: schemas.ProjectCreate,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    # Querying the Project model using project_id
    project_query = db.query(models.Project).filter(models.Project.id == project_id)
    project = project_query.first()

    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"No project found with ID: {project_id}")

    # Check if the user is part of the project using the association table
    association = db.query(models.user_project_association_table).filter(
        models.user_project_association_table.c.user_id == current_user['id'],
        models.user_project_association_table.c.project_id == project_id
    ).first()

    if not association:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You are not part of this project")

    project_query.update(updated_project.dict(), synchronize_session=False)
    db.commit()

    return project_query.first()

    return project_query.first()

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    # Querying the Project model using project_id
    project_query = db.query(models.Project).filter(models.Project.id == project_id)
    project = project_query.first()

    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"No project found with ID: {project_id}")

    # Check if the user is part of the project using the association table
    association = db.query(models.user_project_association_table).filter(
        models.user_project_association_table.c.user_id == current_user['id'],
        models.user_project_association_table.c.project_id == project_id
    ).first()

    if not association:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You are not part of this project")

    project_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


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

    return association_data

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ProjectOut])
def list_all_projects(
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


@router.get("/{project_id}/users", response_model=List[schemas.UserOut])
def list_users_in_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"No project found with ID: {project_id}")

    return project.users



