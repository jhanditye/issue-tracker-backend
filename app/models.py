from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

# Many-to-many association table for User and Projects
user_project_association_table = Table(
    "user_projects",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("projects.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    issues = relationship("Issue", back_populates="assigned_user")
    projects = relationship("Project", secondary=user_project_association_table, back_populates="users")

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    assigned_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    assigned_user = relationship("User", back_populates="issues")
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    project = relationship("Project", back_populates="issues")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    users = relationship("User", secondary=user_project_association_table, back_populates="projects")
    issues = relationship("Issue", back_populates="project")
