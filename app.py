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

    # List all the chapters in order
    chapters = session.query(Sources.chapter).distinct().order_by(Sources.chapter)

    # List all the authors of each book and chapter
    authors = session.query(Sources.author).distinct().order_by(Sources.author)

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

    # Return the data to list.html
    return render_template('list.html',
                           books=books,
                           chapters=chapters,
                           authors=authors,
                           dchapters=dchapters,
                           dverses=dverses,
                           avgdegree=avgdegree,
                           mindegree=mindegree,
                           maxdegree=maxdegree
                           )


@app.route('/')
def home():
    return render_template('home.html')


app.run(host='0.0.0.0', port=5001)

