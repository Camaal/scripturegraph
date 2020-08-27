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
    Author = Column(String(250), nullable=False)
    book_name = Column(String(250), nullable=False)
    testament = Column(String(2), nullable=False)
    genre_name = Column(String(250), nullable=False)
    book = Column(Integer, nullable=False)
    chapter = Column(Integer, nullable=False)
    verse = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    Degree = Column(Integer, nullable=False)

    targets = relationship('References', back_populates="sources")

# The source scripture
class Targets(Base):
    __tablename__ = "target"

    Id = Column(Integer, primary_key=True)
    red_letter = Column(Boolean, nullable=False)
    Author = Column(String(250), nullable=False)
    book_name = Column(String(250), nullable=False)
    testament = Column(String(2), nullable=False)
    genre_name = Column(String(250), nullable=False)
    book = Column(Integer, nullable=False)
    chapter = Column(Integer, nullable=False)
    verse = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    Degree = Column(Integer, nullable=False)

    sources = relationship('References', back_populates="targets")


# Deprecated table that housed all the data (too slow)
# class Network(Base):
#     __tablename__ = "network"
#     Source = Column(Integer, nullable=False)
#     s_red_letter = Column(String(5), nullable=False)
#     s_book_name = Column(String(250), nullable=False)
#     s_book_order = Column(Integer, nullable=False)
#     s_author = Column(String(250), nullable=False)
#     s_author_degree = Column(Integer, nullable=False)
#     s_testament = Column(String(250), nullable=False)
#     s_genre_name = Column(String(250), nullable=False)
#     s_book = Column(Integer, nullable=False)
#     s_chapter = Column(Integer, nullable=False)
#     s_verse = Column(Integer, nullable=False)
#     s_text = Column(Text, nullable=False)
#     s_degree = Column(Integer, nullable=False)
#     Target = Column(Integer, nullable=False)
#     t_red_letter = Column(String(5), nullable=False)
#     t_book_name = Column(String(250), nullable=False)
#     t_book_order = Column(Integer, nullable=False)
#     t_author = Column(String(250), nullable=False)
#     t_author_degree = Column(Integer, nullable=False)
#     t_testament = Column(String(250), nullable=False)
#     t_genre_name = Column(String(250), nullable=False)
#     t_book = Column(Integer, nullable=False)
#     t_chapter = Column(Integer, nullable=False)
#     t_verse = Column(Integer, nullable=False)
#     t_text = Column(Text, nullable=False)
#     t_degree = Column(Integer, nullable=False)
#     Id = Column(Integer, primary_key=True)


engine = create_engine('sqlite:///bible.db', echo=True)

Base.metadata.create_all(engine)
