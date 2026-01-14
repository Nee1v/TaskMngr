from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship #How tables relate to eachother in python objects
from database import Base #Base holds all table metadata

#Association table for many-to-many dependencies
task_dependencies = Table(
    'task_dependencies',
    Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id'), primary_key=True), #Origin task
    Column('depends_on_id', Integer, ForeignKey('tasks.id'), primary_key=True) #Task that Origin task is dependent on
)

#Table containing all tasks
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    completed = Column(Boolean, default=False)
    order = Column(Integer)
    goal = Column(String, nullable=False)

    #Tasks this task depends on
    depends_on = relationship(
        "Task",
        secondary=task_dependencies,
        primaryjoin=id==task_dependencies.c.task_id,
        secondaryjoin=id==task_dependencies.c.depends_on_id,
        backref="dependent_tasks"
    )

