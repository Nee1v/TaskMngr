from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal
from models import Task
from sqlalchemy import and_
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import joinedload, Session

app = FastAPI()

# Allow frontend localhost to access backend
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/tasks/todo")
def get_todo_tasks(goal: str = "Bread", db: Session = Depends(get_db)):
    # Fetch ALL tasks for this goal so we can see statuses of dependencies
    all_goal_tasks = (
        db.query(Task)
        .options(joinedload(Task.depends_on))
        .filter(Task.goal == goal)
        .all()
    )

    tasks_to_return = []
    for task in all_goal_tasks:
        if not task.completed:
            # Task is 'To-Do' only if all its dependencies are completed
            if all(dep.completed for dep in task.depends_on):
                tasks_to_return.append(task)

    return tasks_to_return

@app.get("/tasks/completed")
def get_completed_tasks(goal: str = "Bread", db: Session = Depends(get_db)):
    return (
        db.query(Task)
        .filter(Task.completed == True, Task.goal == goal)
        .all()
    )

@app.post("/tasks/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = True
    db.commit()
    db.refresh(task) # Refresh to ensure we have the latest state
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
    # Find all completed tasks for this goal
    tasks = db.query(Task).filter(Task.goal == goal, Task.completed == True).all()
    
    for task in tasks:
        task.completed = False
        
    db.commit()
    return {"message": f"All tasks for {goal} have been reset"}