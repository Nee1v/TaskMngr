from database import SessionLocal
from models import Task

db = SessionLocal()

# ------------------ Bread Tasks ------------------
add_flour = Task(title="Add flour", description="Add flour to bowl", order=1, goal="Bread")
add_water = Task(title="Add water", description="Add water after flour", order=2, goal="Bread")
add_salt = Task(title="Add salt", description="Add salt after flour", order=3, goal="Bread")
mix = Task(title="Mix ingredients", description="Mix flour, water, salt", order=4, goal="Bread")
preheat = Task(title="Preheat oven", description="Preheat to 350°F", order=1, goal="Bread")
bake = Task(title="Bake", description="Bake the dough", order=5, goal="Bread")

db.add_all([add_flour, add_water, add_salt, mix, preheat, bake])
db.commit()

# Bread dependencies
add_water.depends_on.append(add_flour)
add_salt.depends_on.append(add_flour)
mix.depends_on.extend([add_water, add_salt])
bake.depends_on.extend([mix, preheat])

# ------------------ Pizza Tasks ------------------
pizza_dough = Task(title="Prepare dough", description="Mix flour, yeast, water, salt", order=1, goal="Pizza")
roll_dough = Task(title="Roll dough", description="Flatten the dough", order=2, goal="Pizza")
add_sauce = Task(title="Add sauce", description="Spread tomato sauce on dough", order=3, goal="Pizza")
add_toppings = Task(title="Add toppings", description="Add cheese and toppings", order=4, goal="Pizza")
bake_pizza = Task(title="Bake pizza", description="Bake in oven at 400°F", order=5, goal="Pizza")

db.add_all([pizza_dough, roll_dough, add_sauce, add_toppings, bake_pizza])
db.commit()

# Pizza dependencies
roll_dough.depends_on.append(pizza_dough)
add_sauce.depends_on.append(roll_dough)
add_toppings.depends_on.append(add_sauce)
bake_pizza.depends_on.append(add_toppings)

db.commit()
db.close()

print("Tasks seeded with dependencies for Bread and Pizza")


