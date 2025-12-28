from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
import models
from auth import get_current_user
from database import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    dependencies=[Depends(get_current_user)]
)

@router.get("", response_model=List[models.Task])
def read_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    tasks = db.exec(select(models.Task).where(models.Task.user_id == current_user.id)).all()
    return tasks

@router.post("", response_model=models.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: models.Task, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.put("/{task_id}", response_model=models.Task)
def update_task(task_id: int, task: models.Task, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.get(models.Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
        
    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.get(models.Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
        
    db.delete(db_task)
    db.commit()
    return

@router.patch("/{task_id}/complete", response_model=models.Task)
def toggle_task_completion(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_task = db.get(models.Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if db_task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to toggle this task")
        
    db_task.completed = not db_task.completed
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
