from typing import List,Optional 
from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.params import Body
from app import models, oauth2, schemas
from ..database import get_db
from sqlalchemy.orm import Session

# Routes for Teams
router = APIRouter(
    prefix="/teams",
    tags=['Teams']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TeamOut)
def create_team(
    team: schemas.TeamCreate,
    db: Session = Depends(get_db)
):
    new_team = models.Team(**team.dict())
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team



@router.post("/{team_id}/join", status_code=status.HTTP_200_OK, response_model=schemas.UserTeamAssociation)
def join_team(
    team_id: int,
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    existing_association = db.query(models.user_team_association_table).filter(
        models.user_team_association_table.c.user_id == current_user['id'],
        models.user_team_association_table.c.team_id == team_id
    ).first()

    if existing_association:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User is already part of this team.")

    association_data = {"user_id": current_user['id'], "team_id": team_id}
    db.execute(models.user_team_association_table.insert().values(**association_data))

    # As you're returning an association in the response, 
    # I'm returning the association_data here. 
    # You might need to adjust the response model or the returned data 
    # to make sure it aligns with your `schemas.UserTeamAssociation`.
    return association_data


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.TeamOut])
def list_teams(
    current_user: int = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
    search: Optional[str] = ""
):
    # Using an association table or direct many-to-many field in ORM, 
    # you would retrieve the teams for a user.
    teams = db.query(models.Team).join(models.UserTeamAssociation).filter(
        models.UserTeamAssociation.user_id == current_user['id']
    )

    if search:
        teams = teams.filter(models.Team.name.contains(search))

    return teams.all()
