import logging
import os
import requests
from flask import render_template, request
from app import app, db
from sqlalchemy import func
from app.models import Books, Authors, References, Sources, Targets
import matplotlib as mpl
import matplotlib.cm as cm
from app.graph import getNeighborNetwork


@app.template_filter()
def numberFormat(value):
    return format(int(value), ',d')


@app.template_filter()
def bookColor(value):
    #norm = mpl.colors.Normalize(vmin=400, vmax=120000)
    norm = mpl.colors.Normalize(vmin=10, vmax=90)
    cmap = cm.viridis
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    return format(m.to_rgba(float(value), bytes=True, alpha=1))


@app.template_filter()
def authorColor(value):
    #norm = mpl.colors.Normalize(vmin=600, vmax=220000)
    norm = mpl.colors.Normalize(vmin=1, vmax=100)
    cmap = cm.viridis
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    return format(m.to_rgba(float(value), bytes=True, alpha=1))


@app.template_filter()
def chapterColor(value):
    #norm = mpl.colors.Normalize(vmin=400, vmax=6500)
    norm = mpl.colors.Normalize(vmin=1, vmax=120)
    cmap = cm.viridis
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    return format(m.to_rgba(float(value), bytes=True, alpha=1))


@app.template_filter()
def verseColor(value):
    norm = mpl.colors.Normalize(vmin=0, vmax=200)
    cmap = cm.viridis
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    return format(m.to_rgba(value, bytes=True, alpha=1))


@app.route('/')
@app.route('/index', methods=['POST'])
def index():
    defaultbookname = 'Genesis'
    defaultbook = 1
    defaultchapter = 1
    defaultsource = 1001001

    # List all books in order they were written
    books = db.session.query(Books.bookName).distinct().order_by(Books.book)

    authors = db.session.query(Authors.author, Authors.bookName, Authors.book, Authors.chapter) \
        .order_by(Authors.degree).all()

    # Sum degree for each book
    bookDegrees = db.session.query(Sources.book, Sources.bookName, func.avg(Sources.degree).label('total')) \
        .group_by(Sources.book, Sources.bookName).order_by(Sources.book, Sources.bookName).all()

    # Sum degree for each author
    authorDegrees = db.session.query(Sources.author, func.avg(Sources.degree).label('total')) \
        .group_by(Sources.author).order_by(func.avg(Sources.degree).desc()).all()

    # Sum degree for each chapter
    chapterDegrees = db.session.query(Sources.book, Sources.chapter, func.avg(Sources.degree).label('total')) \
        .group_by(Sources.book, Sources.chapter).order_by(Sources.chapter).filter(Sources.book == defaultbook)

    # List distinct chapters for a given book
    dchapters = db.session.query(Sources.chapter).distinct().filter(Sources.book == defaultbook).count()

    # List chapters, verses, and text for a given book
    dverses = db.session.query(Sources.bookName, Sources.chapter, Sources.verse, Sources.text, Sources.degree,
                               Sources.normDegree, Sources.id).filter(Sources.book == defaultbook,
                                                                                     Sources.chapter == defaultchapter)

    return render_template('index.html',
                           title='Home',
                           defaultbookname=defaultbookname,
                           defaultbook=defaultbook,
                           defaultsource=defaultsource,
                           defaultchapter=defaultchapter,
                           books=books,
                           authors=authors,
                           bookDegrees=bookDegrees,
                           chapterDegrees=chapterDegrees,
                           authorDegrees=authorDegrees,
                           dchapters=dchapters,
                           dverses=dverses
                           )


@app.route('/filter_book_menu', methods=['POST'])
def filter_book_menu():

    filteredbooks = db.session.query(Sources.book, Sources.bookName, func.avg(Sources.degree).label('total')) \
        .group_by(Sources.book, Sources.bookName).order_by(func.avg(Sources.degree).desc()) \
        .filter(Sources.author == request.form['author'])

    return render_template('book_menu.html', filteredbooks=filteredbooks)


@app.route('/filter_chapter_menu', methods=['POST'])
def filter_chapter_menu():
    
    filteredchapters = db.session.query(Sources.book, Sources.chapter,
                                        func.avg(Sources.degree).label('total')).group_by(
        Sources.book, Sources.chapter).order_by(Sources.chapter).filter(Sources.book == request.form['book'])

    return render_template('chapter_menu.html', filteredchapters=filteredchapters)


@app.route('/filter_source', methods=['POST'])
def filter_source():

    filterbook = request.form['book']

    if int(request.form['chapter']) == 0:
        filterchapter = 1
    else:
        filterchapter = request.form['chapter']

    fchapterdegrees = db.session.query(Sources.chapter, func.avg(Sources.degree).label('total')) \
        .group_by(Sources.chapter).order_by(Sources.chapter).filter(Sources.book == filterbook)

    fschapters = db.session.query(Sources.chapter).distinct().filter(Sources.book == filterbook).count()

    fsverses = db.session.query(Sources.chapter, Sources.verse, Sources.text, Sources.degree,
                                Sources.normDegree, Sources.id, Sources.redLetter).filter(
        Sources.book == filterbook, Sources.chapter == filterchapter)

    return render_template('source.html',
                           filterchapter=filterchapter,
                           fschapters=fschapters,
                           fsverses=fsverses,
                           fchapterdegrees=fchapterdegrees)


@app.route('/filter_book_name', methods=['POST'])
def filter_book_name():
    defaultsbookname = db.session.query(Sources.bookName).filter(Sources.book == request.form['book']).first()

    return render_template('source_book_name.html', defaultsbookname=defaultsbookname)


@app.route('/filter_target', methods=['POST'])
def filter_target():

    ftbooks = db.session.query(Targets.book, Targets.bookName, Targets.chapter, Targets.author).distinct().join(
        References).filter(References.source == request.form['id']).order_by(Targets.book).distinct()

    ftverses = db.session.query(Targets.id, Targets.author, Targets.bookName, Targets.book, Targets.chapter,
                                Targets.genreName, Targets.testament,
                                Targets.verse, Targets.text,
                                Targets.degree, Targets.normDegree, Targets.redLetter).join(References) \
        .filter(References.source == request.form['id']).all()

    fsverses = db.session.query(Sources.id, Sources.author, Sources.bookName, Sources.book, Sources.chapter,
                                Sources.genreName, Sources.testament,
                                Sources.verse, Sources.text,
                                Sources.degree, Sources.normDegree, Sources.redLetter).join(References) \
        .filter(References.target == request.form['id']).all()

    ftauthors = db.session.query(Targets.author).join(References) \
        .filter(References.source == request.form['id']).distinct()

    fdata = getNeighborNetwork(int(request.form['id']))

    return render_template('target.html', ftbooks=ftbooks, ftverses=ftverses, ftauthors=ftauthors, fdata=fdata,
                           fsverses=fsverses)


@app.route('/filter_author_menu', methods=['POST'])
def filter_author_menu():
    filteredauthors = db.session.query(Sources.author, func.avg(Sources.degree).label('total')).group_by(
        Sources.author).order_by(func.avg(Sources.degree).desc()).filter(Sources.book == request.form['book'])

    return render_template('author_menu.html', filteredauthors=filteredauthors)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
