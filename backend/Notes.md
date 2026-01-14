Definitions

SQLite
 - The database we use to store our tables

SQLAlchemy
 - Allows us to communicate with SQLite using Python code rather than raw SQL

Session 
 - A session is used to edit (query, update, delete, change) some aspect of the db, we create a session for each set of related tasks as to have a fresh session each time we must edit. *(Dont use one session for all tasks)*

Base
 - Contains all the blueprint tables as metadata