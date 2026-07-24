from sqlmodel import Session, select
from app.task.models import Task
from app.db.config import engine
from fastapi import HTTPException
from app.task.models import *

def create_task(session: Session, new_task: Task):
    task = Task(title=new_task.title, content=new_task.content)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task 
    
def get_all_tasks(session: Session):
    stmt = select(Task)
    tasks = session.exec(stmt)
    return tasks.all()
    

def get_task_by_id(session: Session, task_id: int):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    return task 
    

def update_task(session: Session, task_id: int, new_task: TaskUpdate):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    task.title = new_task.title 
    task.content = new_task.content 
    session.add(task)
    session.commit()
    session.refresh(task)
    return task 
    
def patch_task(session: Session, task_id: int, new_task: TaskPatch):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    if new_task.title is not None:
        task.title = new_task.title 
    if new_task.content is not None:
        task.content = new_task.content 
    session.add(task)
    session.commit()
    session.refresh(task)
    return task 
    
def delete_task(session: Session, task_id: int):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found!")
    session.delete(task)
    session.commit()
    return task 