from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

import sqlalchemy as db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database import Books, References, Scripture, Base


engine = create_engine('sqlite:///bible.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/list')
def showBooks():
    #List all books in order they were written
    books = session.query(Scripture.book_name).distinct().order_by(Scripture.book)

    #List all the chapters in order
    chapters = session.query(Scripture.chapter).distinct().order_by(Scripture.chapter)

    #List all the authors of each book and chapter
    authors = session.query(Scripture.Author).distinct().order_by(Scripture.Author)

    #Calculate the average degree of a given book (eventually replace the book with a variable triggered by a button)
    avgdegree = session.query(func.avg(Scripture.Degree)).filter_by(book=1).all()

    #Calculate min degree
    mindegree = session.query(func.min(Scripture.Degree)).filter_by(book=1).all()

    #Calculate max degree
    maxdegree = session.query(func.max(Scripture.Degree)).filter_by(book=1).all()

    #List distinct chapters for a given book
    dchapters = session.query(Scripture.chapter).distinct().filter_by(book=1).count()

    #List chapters, verses, and text for a given book
    dverses = session.query(Scripture.chapter, Scripture.verse, Scripture.text, Scripture.Degree).filter_by(book=1)

    #references = session.query(References).join(Scripture).filter(Scripture.book==1).all()

    #Return the data to list.html
    return render_template('list.html',
                           books=books,
                           chapters=chapters,
                           authors=authors,
                           dchapters=dchapters,
                           dverses=dverses,
                           avgdegree=avgdegree,
                           mindegree=mindegree,
                           maxdegree=maxdegree,
                           #references=references
                           )


@app.route('/')
def home():
    return render_template('home.html')

app.run(host='0.0.0.0', port=5000)