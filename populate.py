from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Books, References, Sources, Targets, Base

engine = create_engine('sqlite:///cm_bible.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()
