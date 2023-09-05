from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

# Many-to-many association table for User and Teams
user_team_association_table = Table(
    "user_teams",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("team_id", Integer, ForeignKey("teams.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    issues = relationship("Issue", back_populates="assigned_user")
    teams = relationship("Team", secondary=user_team_association_table, back_populates="users")

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    assigned_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    assigned_user = relationship("User", back_populates="issues")
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    team = relationship("Team", back_populates="issues")

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    users = relationship("User", secondary=user_team_association_table, back_populates="teams")
    issues = relationship("Issue", back_populates="team")
