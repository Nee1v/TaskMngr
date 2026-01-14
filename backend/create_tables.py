from database import engine #Import the engine from database.py so we can tell SQLite where to create the tables (DB URL is from engine)
from models import Base #Essentially base contains all the table blueprints, without base we arent able to create our desired tables

Base.metadata.create_all(bind=engine) #Tells SQLite to create all the tables in the base metadata
print("Tables created")
