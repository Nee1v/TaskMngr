from database import SessionLocal
from models import Task

def print_todo_and_completed():
    db = SessionLocal()
    todo_tasks = []
    all_tasks = db.query(Task).filter(Task.completed == False).all()
    for task in all_tasks:
        if all(dep.completed for dep in task.depends_on):
            todo_tasks.append(task)

    completed_tasks = db.query(Task).filter(Task.completed == True).all()

    print("\nTODO Tasks:")
    for t in todo_tasks:
        print(f"- {t.title}")

    print("\nCompleted Tasks:")
    for t in completed_tasks:
        print(f"- {t.title}")

    db.close()

def complete_task(title):
    db = SessionLocal()
    task = db.query(Task).filter(Task.title == title).first()
    if task:
        task.completed = True
        db.commit()
        print(f"\nTask '{title}' marked as completed.")
    else:
        print(f"\nTask '{title}' not found.")
    db.close()

if __name__ == "__main__":
    print("Initial state:")
    print_todo_and_completed()

    # Simulate completing tasks step by step
    steps = ["Add flour", "Preheat oven", "Add water", "Add salt", "Mix ingredients", "Bake"]
    for step in steps:
        input(f"\nPress Enter to complete '{step}'...")  # Wait for user input
        complete_task(step)
        print_todo_and_completed()
