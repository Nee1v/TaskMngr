from database import SessionLocal
from models import Task

db = SessionLocal()

def seed_data():
    # Optional: Clear existing tasks to start fresh
    db.query(Task).delete()
    db.commit()

    # ------------------ Bread Tasks ------------------
    add_flour = Task(title="Add flour", description="Add flour to bowl", order=1, goal="Bread")
    add_water = Task(title="Add water", description="Add water after flour", order=2, goal="Bread")
    add_salt = Task(title="Add salt", description="Add salt after flour", order=3, goal="Bread")
    mix = Task(title="Mix ingredients", description="Mix flour, water, salt", order=4, goal="Bread")
    preheat_bread = Task(title="Preheat oven", description="Preheat to 350°F", order=1, goal="Bread")
    bake_bread = Task(title="Bake", description="Bake the dough", order=5, goal="Bread")

    db.add_all([add_flour, add_water, add_salt, mix, preheat_bread, bake_bread])
    db.commit()

    # Bread dependencies
    add_water.depends_on.append(add_flour)
    add_salt.depends_on.append(add_flour)
    mix.depends_on.extend([add_water, add_salt])
    bake_bread.depends_on.extend([mix, preheat_bread])

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

    # ------------------ Cake Tasks (20 Concurrent Tasks) ------------------
    cake_items = [
        ("Get Flour", "Need 2 cups of all-purpose flour"),
        ("Get Sugar", "Need 1.5 cups of granulated sugar"),
        ("Get Cocoa Powder", "Need 3/4 cup of unsweetened cocoa"),
        ("Get Baking Powder", "Need 2 teaspoons"),
        ("Get Baking Soda", "Need 1.5 teaspoons"),
        ("Get Salt", "Need 1 teaspoon"),
        ("Get Eggs", "Need 2 large eggs at room temperature"),
        ("Get Milk", "Need 1 cup of whole milk"),
        ("Get Vegetable Oil", "Need 1/2 cup"),
        ("Get Vanilla Extract", "Need 2 teaspoons"),
        ("Get Boiling Water", "Need 1 cup for the batter"),
        ("Get Butter", "For the frosting (2 sticks)"),
        ("Get Powdered Sugar", "4 cups for the frosting"),
        ("Get Heavy Cream", "For the frosting consistency"),
        ("Find Large Bowl", "Main mixing bowl"),
        ("Find Medium Bowl", "For whisking wet ingredients"),
        ("Find Whisk", "To remove lumps from dry ingredients"),
        ("Find Spatula", "To scrape the sides of the bowl"),
        ("Find Cake Pans", "Two 9-inch round pans"),
        ("Find Cooling Rack", "To let the layers breathe after baking")
    ]

    for title, desc in cake_items:
        task = Task(title=title, description=desc, goal="Cake")
        db.add(task)

    db.commit()
    print("Successfully seeded Bread, Pizza, and a long Cake quest!")

if __name__ == "__main__":
    seed_data()
    db.close()