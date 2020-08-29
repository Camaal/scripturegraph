import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()











engine = create_engine('sqlite:///cm_bible.db', connect_args={'check_same_thread': False})


Base.metadata.create_all(engine)
