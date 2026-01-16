from database import SessionLocal
from models import Task

db = SessionLocal()

def seed_data():
    db.query(Task).delete()
    db.commit()

    # Create a master list to hold everything
    all_tasks = []

    # ------------------ ORIGINS: GENERATORS ------------------
    for i in range(1, 7):
        desc_map = {
            1: "Spawn area", 2: "Near Tank Station", 3: "Near the Shield door",
            4: "At Juggernog", 5: "At Stamin-Up", 6: "At the Church"
        }
        all_tasks.append(Task(
            title=f"Power on Gen {i}", 
            description=f"Capture Generator {i} ({desc_map[i]})", 
            goal="Origins"
        ))

    # ------------------ ORIGINS: MAXIS DRONE ------------------
    d_rotor = Task(
        title="Collect Maxis Drone Rotor", 
        description="Top of mound, Left of gramophone table, OR Bottom level of excavation scaffolding.", 
        goal="Origins"
    )
    d_brain = Task(
        title="Collect Maxis Drone Brain", 
        description="On bench as soon as you spawn (Gen 1)", 
        goal="Origins"
    )
    d_frame = Task(
        title="Collect Maxis Drone Frame", 
        description="Tank exit path out of church, Tank return path, OR Bottom of ice tunnel.", 
        goal="Origins"
    )

    build_drone = Task(
        title="Build Maxis Drone", 
        description="Use the collected parts at any workbench.", 
        goal="Origins"
    )
    
    build_drone.depends_on.extend([d_rotor, d_brain, d_frame])

    #Add the drone tasks to our master list
    all_tasks.extend([d_rotor, d_brain, d_frame, build_drone])

    # ------------------ FINAL COMMIT ------------------
    #Add everything in one go
    db.add_all(all_tasks)
    db.commit()
    
    print(f"Origins seeded: {len(all_tasks)} tasks added successfully.")

if __name__ == "__main__":
    seed_data()
    db.close()