from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

# ✅ YEH HAI FIX: Signup ke liye JSON Model
class UserCreate(SQLModel):
    email: str
    password: str

# Login Token Response
class Token(SQLModel):
    access_token: str
    token_type: str

# Database Table: User
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str

    tasks: List["Task"] = Relationship(back_populates="user")

# Database Table: Task
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="tasks")