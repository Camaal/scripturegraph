from flask import Flask, render_template, url_for, request

from app import app, db
from sqlalchemy import func
from app.models import Books, Authors, References, Sources, Targets
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

@app.route('/')
@app.route('/index')
def index():

    # List all books in order they were written
    books = db.session.query(Books.book_name).distinct().order_by(Books.book)

    authors = db.session.query(Authors.author, Authors.book_name, Authors.book, Authors.chapter)\
        .order_by(Authors.book).all()

    # Sum degree for each book
    bookDegrees = db.session.query(Sources.book, Sources.book_name, func.sum(Sources.degree).label('total')).group_by(
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
    dverses = db.session.query(Sources.chapter, Sources.verse, Sources.text, Sources.degree, Sources.color,
                               Sources.norm_degree).filter_by(book=1)

    # List book, book name, and chapter for cross-references related to Gen 1:1
    tbooks = db.session.query(Targets.book, Targets.book_name, Targets.chapter, Targets.author).distinct().join(
        References).filter(
        References.Source == 1001001).order_by(Targets.book).distinct()

    # List book, book name, chapter, verse, text and degree for cross-references related to Gen 1:1
    joins = db.session.query(Targets.book_name, Targets.book, Targets.chapter, Targets.verse, Targets.text,
                             Targets.degree, Targets.color, Targets.norm_degree).join(References) \
        .filter(References.Source == 1001001).all()

    # List authors related to Gen 1:1
    tauthors = db.session.query(Targets.author).join(References) \
        .filter(References.Source == 1001001).distinct()

    # Return the data to index.html

    return render_template('index.html',
                           title='Home',
                           books=books,
                           authors=authors,
                           bookDegrees=bookDegrees,
                           chapterDegrees=chapterDegrees,
                           authorDegrees=authorDegrees,
                           dchapters=dchapters,
                           dverses=dverses,
                           tbooks=tbooks,
                           joins=joins,
                           tauthors=tauthors
                           )


@app.route('/filter_book_menu', methods=['POST'])
def filter_book_menu():

    filteredbooks = db.session.query(Sources.book, Sources.book_name, func.sum(Sources.degree).label('total')).group_by(
        Sources.book_name).order_by(Sources.book).filter_by(author = request.form['author'])

    return render_template('book_menu.html', filteredbooks=filteredbooks)
