from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

# ✅ FIX 1: UserCreate class add ki gayi hai (Signup ke liye zaroori)
class UserCreate(SQLModel):
    email: str
    password: str

# ✅ FIX 2: Token class add ki gayi hai (Login response ke liye)
class Token(SQLModel):
    access_token: str
    token_type: str

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str

    tasks: List["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="tasks")