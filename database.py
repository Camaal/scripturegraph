import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Book of the Bible


class Books(Base):
    __tablename__ = "books"

    book_name = Column(String(250), nullable=False)
    testament = Column(String(2), nullable=False)
    genre_name = Column(String(250), nullable=False)
    book = Column(Integer, primary_key=True)


class References(Base):
    __tablename__ = "references"

    Id = Column(Integer, primary_key=True)
    Source = Column(Integer, ForeignKey('source.Id'))
    Target = Column(Integer, ForeignKey('target.Id'))

# The source scripture


class Sources(Base):
    __tablename__ = "source"

    Id = Column(Integer, primary_key=True)
    red_letter = Column(Boolean, nullable=False)
    author = Column(String(250), nullable=False)
    book_name = Column(String(250), nullable=False)
    testament = Column(String(2), nullable=False)
    genre_name = Column(String(250), nullable=False)
    book = Column(Integer, nullable=False)
    chapter = Column(Integer, nullable=False)
    verse = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    degree = Column(Integer, nullable=False)

# The source scripture


class Targets(Base):
    __tablename__ = "target"

    Id = Column(Integer, primary_key=True)
    red_letter = Column(Boolean, nullable=False)
    author = Column(String(250), nullable=False)
    book_name = Column(String(250), nullable=False)
    testament = Column(String(2), nullable=False)
    genre_name = Column(String(250), nullable=False)
    book = Column(Integer, nullable=False)
    chapter = Column(Integer, nullable=False)
    verse = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    degree = Column(Integer, nullable=False)


engine = create_engine('sqlite:///cm_bible.db')


Base.metadata.create_all(engine)
