from typing import List, Optional
from fastapi import Depends, Response, status, HTTPException, APIRouter
from fastapi.params import Body
from app import models, oauth2, schemas
from ..database import get_db, engine, cursor, conn
from app.schemas import IssueCreate
from sqlalchemy.orm import Session

### Routes for Issues

router = APIRouter(
    prefix="/issues",
    tags=['Issues']
)

@router.get("/", response_model=List[schemas.Issue])
def get_issues(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    issues = db.query(models.Issue).filter(models.Issue.title.contains(search)).limit(limit).offset(skip).all()
    return issues

@router.post("/{project_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Issue)
def create_issue(
    project_id: int,
    issue: schemas.IssueCreate,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    # Check if the user is part of the project
    association = db.query(models.user_project_association_table).filter(
        models.user_project_association_table.c.user_id == current_user['id'],
        models.user_project_association_table.c.project_id == project_id
    ).first()

    if not association:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You are not part of this project")

    new_issue = models.Issue(project_id = project_id,assigned_user_id=current_user['id'], **issue.dict())
    db.add(new_issue)
    db.commit()
    db.refresh(new_issue)
    return new_issue

@router.get("/{project_id}/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Issue)
def get_issue(
    project_id: int,
    id: int,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    issue = db.query(models.Issue).filter(models.Issue.id == id, models.Issue.project_id == project_id).first()
    if not issue:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"No issue found with ID: {id} in project: {project_id}")
    return issue

@router.delete("/{project_id}/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(
    project_id: int,
    id: int,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    issue_query = db.query(models.Issue).filter(models.Issue.id == id, models.Issue.project_id == project_id)
    issue = issue_query.first()
    if not issue:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"No issue found with ID: {id} in project: {project_id}")
    if issue.assigned_user_id != current_user['id']:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You are not the owner of this issue")

    issue_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{project_id}/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Issue)
def update_issue(
    project_id: int,
    id: int,
    updated_issue: IssueCreate,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    issue_query = db.query(models.Issue).filter(models.Issue.id == id, models.Issue.project_id == project_id)
    issue = issue_query.first()

    if issue is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"No issue found with ID: {id} in project: {project_id}")
    if issue.assigned_user_id != current_user['id']:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You are not the owner of this issue")

    issue_query.update(updated_issue.dict(), synchronize_session=False)
    db.commit()

    return issue_query.first()
