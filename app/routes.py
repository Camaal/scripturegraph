from flask import Flask, render_template, url_for, request, flash, redirect

from app import app, db
from sqlalchemy import func
from app.models import References, Sources, Targets
import matplotlib as mpl
import matplotlib.cm as cm


@app.template_filter()
def numberFormat(value):
    return format(int(value), ',d')

@app.template_filter()
def degreeColor(value):
    norm = mpl.colors.Normalize(vmin=.04, vmax=1)
    cmap = cm.viridis
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    return format(m.to_rgba(value, bytes=True))

def flat_list(l):
    return ["%s" % v for v in l]


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    # List all books in order they were written
    books = db.session.query(Sources.book_name).distinct().order_by(Sources.book)

    # List all the chapters in order
    chapters = db.session.query(Sources.chapter).distinct().order_by(Sources.chapter)

    # List all the authors of each book and chapter
    authors = db.session.query(Sources.author).distinct().order_by(Sources.author)

    # Sum degree for each book
    bookDegrees = db.session.query(Sources.book_name, func.sum(Sources.degree).label('total')).group_by(
        Sources.book_name).order_by(Sources.book).all()

    # Sum degree for each chapter
    chapterDegrees = db.session.query(Sources.chapter, func.sum(Sources.degree).label('total')).group_by(
        Sources.chapter).order_by(Sources.chapter).all()

    # Sum degree for each chapter
    authorDegrees = db.session.query(Sources.author, func.sum(Sources.degree).label('total')).group_by(
        Sources.author).order_by(Sources.author).all()

    # List distinct chapters for a given book
    dchapters = db.session.query(Sources.chapter).distinct().filter_by(book=1).count()

    # List chapters, verses, and text for a given book
    dverses = db.session.query(Sources.chapter, Sources.verse, Sources.text, Sources.degree, Sources.color, Sources.norm_degree).filter_by(book=1)

    # List book, book name, and chapter for cross-references related to Gen 1:1
    tbooks = db.session.query(Targets.book, Targets.book_name, Targets.chapter, Targets.author).distinct().join(
        References).filter(
        References.Source == 1001001).all()

    # List book, book name, chapter, verse, text and degree for cross-references related to Gen 1:1
    joins = db.session.query(Targets.book_name, Targets.book, Targets.chapter, Targets.verse, Targets.text,
                    Targets.degree, Targets.color, Targets.norm_degree).join(References).filter(References.Source == 1001001).all()

    # Return the data to index.html

    return render_template('index.html',
                           title='Home',
                           books=books,
                           chapters=chapters,
                           authors=authors,
                           dchapters=dchapters,
                           dverses=dverses,
                           joins=joins,
                           tbooks=tbooks,
                           bookDegrees=bookDegrees,
                           chapterDegrees=chapterDegrees,
                           authorDegrees=authorDegrees
                           )