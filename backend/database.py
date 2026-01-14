from sqlalchemy import create_engine #The create_engine is used as our connection to the database, it is how we communicate with the DB
from sqlalchemy.orm import sessionmaker, declarative_base #sessionmaker is used to create all the sessions we use to edit the db, 
# and declaritive_base is the Base class the contains all the table blueprints

DATABASE_URL = "sqlite:///./tasks.db" #Location of database, uses sqlite, db name is "tasks", file name "tasks.db"

engine = create_engine( #The engine is the object that allows us to connect to the db
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False, #Changes are ony commited when db.commit() is called
    autoflush=False, #Changes are not automatically pushed to the DB unless commit() is called
    bind=engine #Use tasks.db engine
)

Base = declarative_base() #Base contains all relevant tables in base metadata for future use
