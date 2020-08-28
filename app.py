from flask import Flask, render_template, url_for, request

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database import Books, References, Sources, Targets, Base

engine = create_engine('sqlite:///cm_bible.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/list')
def showBooks():
    # List all books in order they were written
    books = session.query(Sources.book_name).distinct().order_by(Sources.book)

    # Sum degree for each book
    bookDegrees = session.query(Sources.book_name, func.sum(Sources.degree).label('total')).group_by(
        Sources.book_name).order_by(Sources.book).all()

    # List all the chapters in order
    chapters = session.query(Sources.chapter).distinct().order_by(Sources.chapter)

    # Sum degree for each chapter
    chapterDegrees = session.query(Sources.chapter, func.sum(Sources.degree).label('total')).group_by(
        Sources.chapter).order_by(Sources.chapter).all()

    # List all the authors of each book and chapter
    authors = session.query(Sources.author).distinct().order_by(Sources.author)

    # Sum degree for each chapter
    authorDegrees = session.query(Sources.author, func.sum(Sources.degree).label('total')).group_by(
        Sources.author).order_by(Sources.author).all()

    # Calculate the average degree of a given book (eventually replace the book with a variable triggered by a button)
    avgdegree = session.query(func.avg(Sources.degree)).filter_by(book=1).all()

    # Calculate min degree
    mindegree = session.query(func.min(Sources.degree)).filter_by(book=1).all()

    # Calculate max degree
    maxdegree = session.query(func.max(Sources.degree)).filter_by(book=1).all()

    # List distinct chapters for a given book
    dchapters = session.query(Sources.chapter).distinct().filter_by(book=1).count()

    # List chapters, verses, and text for a given book
    dverses = session.query(Sources.chapter, Sources.verse, Sources.text, Sources.degree).filter_by(book=1)

    # List book, book name, and chapter for cross-references related to Gen 1:1
    tbooks = session.query(Targets.book, Targets.book_name, Targets.chapter).distinct().join(References).filter(
        References.Source == 1001001).all()

    # List book, book name, chapter, verse, text and degree for cross-references related to Gen 1:1
    joins = session.query(Targets.book_name, Targets.book, Targets.chapter, Targets.verse, Targets.text,
                          Targets.degree).join(References).filter(References.Source == 1001001).all()

    # Return the data to list.html.jinja

    return render_template('list.html.jinja',
                           books=books,
                           chapters=chapters,
                           authors=authors,
                           dchapters=dchapters,
                           dverses=dverses,
                           avgdegree=avgdegree,
                           mindegree=mindegree,
                           maxdegree=maxdegree,
                           joins=joins,
                           tbooks=tbooks,
                           bookDegrees=bookDegrees,
                           chapterDegrees=chapterDegrees,
                           authorDegrees=authorDegrees
                           )


@app.route('/')
def home():
    return render_template('home.html.jinja')


app.run(host='0.0.0.0', port=5000)
