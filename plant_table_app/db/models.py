""" Module sets up the database tables using SQLAlchemy"""

# tk_sql_app/db/models.py

from sqlalchemy import (
    Column, ForeignKey, ForeignKeyConstraint, Table, UniqueConstraint, event,
    Boolean, Date, Integer, Text, String
)
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.util import unwrap_order_by

Base = declarative_base()

# Sets up a link table with activity_id and person_id as foreign keys
# Base.metadata is a container object that keeps together many different features of the database
plant_pest = Table('plant_pest',
                   Base.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('plant_id', ForeignKey('plant.id')),
                   Column('pest_id', ForeignKey('pest.id')),
                   UniqueConstraint('pest_id', 'pest_id')
                   )


# Sets up Plant table, this references "pests" via the pest_light table
class Plant(Base):
    __tablename__ = 'plant'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    chem_remove_val = Column(Integer, nullable=False)
    ease_of_growth = Column(Integer, nullable=False)
    care_instructions = Column(String, default="")
    min_temp = Column(Integer, default=15)
    max_temp = Column(Integer, default=25)
    pests = relationship("Pest",
                         secondary=plant_pest,
                         back_populates="plants")

    # Add an ordering above if necessary
    #                         order_by='(Person.last_name, Person.first_name)',
    # Gives a representation of an Activity (for printing out)
    def __repr__(self):
        return f"<Plant({self.name})>"


# Sets up a Person table, this references "activities" via the person_activities table
class Pest(Base):
    __tablename__ = 'pest'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    solution = Column(String, nullable=False)
    plants = relationship("Plant",
                          secondary=plant_pest,
                          order_by='Plant.name',
                          back_populates="pests")

    # Gives a representation of a Person (for printing out)
    def __repr__(self):
        return f"<Pest({self.name})>"
