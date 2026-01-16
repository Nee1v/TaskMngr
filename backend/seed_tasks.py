from database import SessionLocal
from models import Task

db = SessionLocal()

def seed_data():
    #Clear ALL existing tasks to start fresh
    db.query(Task).delete()
    db.commit()

    # ------------------ ORIGINS EASTER EGG ------------------
    
    gen1 = Task(title="Power on Gen 1", description="Capture Generator 1 in Spawn area", goal="Origins")
    gen2 = Task(title="Power on Gen 2", description="Capture Generator 2 near Tank Station", goal="Origins")
    gen3 = Task(title="Power on Gen 3", description="Capture Generator 3 near the Shield door", goal="Origins")
    gen4 = Task(title="Power on Gen 4", description="Capture Generator 4 at Juggernog", goal="Origins")
    gen5 = Task(title="Power on Gen 5", description="Capture Generator 5 at Stamin-Up", goal="Origins")
    gen6 = Task(title="Power on Gen 6", description="Capture Generator 6 at the Church", goal="Origins")

    db.add_all([gen1, gen2, gen3, gen4, gen5, gen6])
    
    # --------------------------------------------------------

    db.commit()
    print("Database cleared. Origins seeded with 6 individual Generator tasks.")

if __name__ == "__main__":
    seed_data()
    db.close()