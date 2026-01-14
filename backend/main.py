from fastapi import FastAPI #FastAPI creates the web app skeleton and define API routes, it also handles the oncoming http requests and what code to run
from database import SessionLocal #Import the Session factory from database, we need this to communicate and edit the db
from models import Task #Task is the table blueprint
from sqlalchemy import and_
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from sqlalchemy.orm import joinedload

app = FastAPI() #Create fastAPI instance, this is our web server

#Allow frontend localhost to access backend
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#If someone visits "http://127.0.0.1:8000/" locally return status ok
@app.get("/") #Define how fastAPI reacts to an endpoint visitor locally, the "/" means they visited the homepage/root of the web app
def root(): #Run root() when someone visits homepage locally
    return {"status": "ok"}

@app.get("/tasks/todo")
def get_todo_tasks(goal: str = "Bread"):
    db = SessionLocal()
    try:
        all_tasks = (
            db.query(Task)
            .options(joinedload(Task.depends_on))  # <--- eager load dependencies
            .filter(Task.completed == False, Task.goal == goal)
            .all()
        )

        tasks = []
        for task in all_tasks:
            if all(dep.completed for dep in task.depends_on):
                tasks.append(task)

        return tasks
    finally:
        db.close()

@app.get("/tasks/completed")
def get_completed_tasks(goal: str = "Bread"):
    db = SessionLocal()
    try:
        return (
            db.query(Task)
            .filter(Task.completed == True, Task.goal == goal)
            .all()
        )
    finally:
        db.close()

@app.post("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        task.completed = True
        db.commit()
        return {"message": f"Task '{task.title}' marked as completed"}
    finally:
        db.close()

@app.post("/tasks/{task_id}/undo")
def undo_task(task_id: int):
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        task.completed = False
        db.commit()
        return {"message": f"Task '{task.title}' marked as incomplete"}
    finally:
        db.close()


