""" File to start-up the database in a console for testing purposes """

# tk_sql_app/console/startup.py
import pathlib

from plant_table_app import db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from plant_table_app.settings import ROOT_DIR
import plant_table_app.db.models as m

sql_path = pathlib.Path(ROOT_DIR).joinpath('var', 'db.sqlite')
engine = create_engine(f'sqlite:///{pathlib.Path(sql_path)}', echo=True)
Session = sessionmaker(bind=engine)

session = Session()
plants = session.query(m.Plant).all()
pests = session.query(m.Pest).all()
daf = plants[0]

# Remember to use session.close() in console when you have finished testing
