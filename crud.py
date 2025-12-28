from sqlmodel import Session, select
from typing import Optional, List
from models import Task, User
from datetime import datetime, timedelta

def get_recent_task_by_title(db: Session, title: str, user_id: int) -> Optional[Task]:
    """
    Checks for a task with the same title created in the last 2 seconds.
    """
    two_seconds_ago = datetime.utcnow() - timedelta(seconds=2)
    return db.exec(
        select(Task).where(
            Task.title == title,
            Task.user_id == user_id,
            Task.created_at > two_seconds_ago
        )
    ).first()

def create_task(db: Session, title: str, description: Optional[str], user_id: int):
    new_task = Task(title=title, description=description, user_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks(db: Session, user_id: int, completed: Optional[bool] = None) -> List[Task]:
    query = select(Task).where(Task.user_id == user_id)
    if completed is not None:
        query = query.where(Task.completed == completed)
    tasks = db.exec(query).all()
    return tasks

def delete_task(db: Session, task_id: int, user_id: int):
    task = db.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
    if task:
        db.delete(task)
        db.commit()
        return {"message": f"Task {task_id} deleted successfully."}
    return None

def update_task(db: Session, task_id: int, user_id: int, completed: Optional[bool] = None, title: Optional[str] = None, description: Optional[str] = None):
    task = db.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
    if task:
        if completed is not None:
            task.completed = completed
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    return None
