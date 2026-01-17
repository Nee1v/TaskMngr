from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal
from models import Task
from sqlalchemy import and_
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import joinedload, Session

app = FastAPI()

#Allow frontend localhost to access backend
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#When visiting home page simply return status ok
@app.get("/")
def root():
    return {"status": "ok"}

#For tasks/todo path
@app.get("/tasks/todo")
def get_todo_tasks(goal: str, db: Session = Depends(get_db)):
    #Get all incomplete tasks for this goal
    tasks = db.query(Task).filter(Task.goal == goal, Task.completed == False).all()
    
    available_tasks = []
    for task in tasks:
        #A task is "Available" if all its dependencies are completed
        if all(dep.completed for dep in task.depends_on):
            available_tasks.append({
                "id": task.id,
                "title": task.title,
                "description": task.description
            })
            
    return available_tasks

#Recursively build a tree of dependencies, so we can fold layers into most dependent task
def build_task_tree(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "sub_tasks": [build_task_tree(sub) for sub in task.depends_on if sub.completed]
    }

@app.get("/tasks/completed")
def get_completed_tasks(goal: str, db: Session = Depends(get_db)):
    all_completed = db.query(Task).filter(Task.goal == goal, Task.completed == True).all()
    
    #Identify which tasks are "children" (dependencies) of others
    child_ids = set()
    for task in all_completed:
        for dep in task.depends_on:
            child_ids.add(dep.id)

    #Only return the "Root" tasks (those not inside another folder)
    #The build_task_tree function will handle nesting everything else inside them
    root_tasks = [
        build_task_tree(task) for task in all_completed 
        if task.id not in child_ids
    ]
    return root_tasks

@app.post("/tasks/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = True
    db.commit()
    db.refresh(task) #Refresh to ensure we have the latest state
    return {"message": f"Task '{task.title}' marked as completed"}

@app.post("/tasks/{task_id}/undo")
def undo_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = False
    db.commit()
    db.refresh(task)
    return {"message": f"Task '{task.title}' marked as incomplete"}

@app.post("/tasks/reset/{goal}")
def reset_goal_tasks(goal: str, db: Session = Depends(get_db)):
    #Find all completed tasks for this goal
    tasks = db.query(Task).filter(Task.goal == goal, Task.completed == True).all()
    
    for task in tasks:
        task.completed = False
        
    db.commit()
    return {"message": f"All tasks for {goal} have been reset"}