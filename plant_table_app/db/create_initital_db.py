""" Code to create the initial database and populate with some test data"""

# tk_sql_app/db/create_initial_db.py

import os
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from plant_table_app.db import models as m
from plant_table_app.settings import ROOT_DIR


# Deletes the current database and creates a new one based on the table information in models.py (m)
def create_new_db():
    print("Deleting current database and starting new")

    sql_path = pathlib.Path(ROOT_DIR).joinpath('var', 'db.sqlite')
    if os.path.exists(sql_path):
        os.remove(sql_path)

    engine = create_engine(f'sqlite:///{pathlib.Path(sql_path)}', echo=True)
    m.Base.metadata.create_all(engine)

    return sessionmaker(bind=engine)


def populate_database(sess):
    # Create new plants
    plants = [m.Plant(name="daffodil",
                      chem_remove_val=4,
                      ease_of_growth=7,
                      care_instructions="Plant bulb in October")
              ]
    # Create some pests
    pests = [m.Pest(name="mealybug",
                    solution="wipe leaves with detergent")
             ]

    # Add relationships
    plants[0].pests.append(pests[0])

    sess.add_all(plants + pests)
    sess.commit()


if __name__ == "__main__":
    Session = create_new_db()
    with Session() as session:
        populate_database(session)
