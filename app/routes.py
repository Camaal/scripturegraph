from flask import Flask, render_template, url_for, request, jsonify, json

import json
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
def degreeColor(value):
    norm = mpl.colors.Normalize(vmin=.04, vmax=1)
    cmap = cm.viridis
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    return format(m.to_rgba(value, bytes=True))

def flat_list(l):
    return ["%s" % v for v in l]

@app.route('/')
@app.route('/index', methods=['POST'])
def index():

    defaultbookname = 'Genesis'
    defaultbook = 1
    defaultsource = 1001001

    # List all books in order they were written
    books = db.session.query(Books.book_name).distinct().order_by(Books.book)

    authors = db.session.query(Authors.author, Authors.book_name, Authors.book, Authors.chapter)\
        .order_by(Authors.degree).all()

    # Sum degree for each book
    bookDegrees = db.session.query(Sources.book, Sources.book_name, func.sum(Sources.degree).label('total'))\
        .group_by(Sources.book_name).order_by(Sources.book).all()

    # Sum degree for each chapter
    authorDegrees = db.session.query(Sources.author, func.sum(Sources.degree).label('total'))\
        .group_by(Sources.author).order_by(func.sum(Sources.degree).desc()).all()

    # Sum degree for each chapter
    chapterDegrees = db.session.query(Sources.chapter, func.sum(Sources.degree).label('total'))\
        .group_by(Sources.chapter).order_by(Sources.chapter).filter_by(book=defaultbook)

    # List distinct chapters for a given book
    dchapters = db.session.query(Sources.chapter).distinct().filter_by(book=defaultbook).count()

    # List chapters, verses, and text for a given book
    dverses = db.session.query(Sources.book_name, Sources.chapter, Sources.verse, Sources.text, Sources.degree,
                               Sources.color, Sources.norm_degree, Sources.Id).filter_by(book=defaultbook)

    # List book, book name, and chapter for cross-references related to Gen 1:1
    tbooks = db.session.query(Targets.book, Targets.book_name, Targets.chapter, Targets.author)\
        .distinct().join(References).filter(References.Source == defaultsource).order_by(Targets.book).distinct()

    # List book, book name, chapter, verse, text and degree for cross-references related to Gen 1:1
    joins = db.session.query(Targets.book_name, Targets.book, Targets.chapter, Targets.verse, Targets.text,
                             Targets.degree, Targets.color, Targets.norm_degree).join(References) \
        .filter(References.Source == defaultsource).all()

    # List authors related to Gen 1:1
    tauthors = db.session.query(Targets.author).join(References) \
        .filter(References.Source == defaultsource).distinct()

    data = getNeighborNetwork(defaultsource)

    # Return the data to index.html
    return render_template('index.html',
                           title='Home',
                           defaultbookname=defaultbookname,
                           defaultbook=defaultbook,
                           defaultsource=defaultsource,
                           books=books,
                           authors=authors,
                           bookDegrees=bookDegrees,
                           chapterDegrees=chapterDegrees,
                           authorDegrees=authorDegrees,
                           dchapters=dchapters,
                           dverses=dverses,
                           tbooks=tbooks,
                           joins=joins,
                           tauthors=tauthors,
                           data=data
                           )


@app.route('/filter_book_menu', methods=['POST'])
def filter_book_menu():

    filteredbooks = db.session.query(Sources.book, Sources.book_name, func.sum(Sources.degree).label('total'))\
        .group_by(Sources.book_name).order_by(func.sum(Sources.degree).desc())\
        .filter_by(author=request.form['author'])

    return render_template('book_menu.html', filteredbooks=filteredbooks)


@app.route('/filter_chapter_menu', methods=['POST'])
def filter_chapter_menu():

    filteredchapters = db.session.query(Sources.chapter, func.sum(Sources.degree).label('total')).group_by(
        Sources.chapter).order_by(Sources.chapter).filter_by(book=request.form['book'])

    return render_template('chapter_menu.html', filteredchapters=filteredchapters)


@app.route('/filter_source', methods=['POST'])
def filter_source():

    fchapterdegrees = db.session.query(Sources.chapter, func.sum(Sources.degree).label('total'))\
        .group_by(Sources.chapter).order_by(Sources.chapter).filter_by(book=request.form['book'])

    fschapters = db.session.query(Sources.chapter).distinct().filter_by(book=request.form['book']).count()

    fsverses = db.session.query(Sources.chapter, Sources.verse, Sources.text, Sources.degree, Sources.color,
                               Sources.norm_degree, Sources.Id).filter_by(book=request.form['book'])

    return render_template('source.html', fschapters=fschapters, fsverses=fsverses, fchapterdegrees=fchapterdegrees)


@app.route('/filter_book_name', methods=['POST'])
def filter_book_name():

    defaultsbookname = db.session.query(Sources.book_name).filter_by(book=request.form['book']).first()

    return render_template('source_book_name.html', defaultsbookname=defaultsbookname)


@app.route('/filter_target', methods=['POST'])
def filter_target():

    ftbooks = db.session.query(Targets.book, Targets.book_name, Targets.chapter, Targets.author).distinct().join(
        References).filter(References.Source == request.form['Id']).order_by(Targets.book).distinct()

    ftverses = db.session.query(Targets.book_name, Targets.book, Targets.chapter, Targets.verse, Targets.text,
                             Targets.degree, Targets.color, Targets.norm_degree).join(References) \
        .filter(References.Source == request.form['Id']).all()

    ftauthors = db.session.query(Targets.author).join(References) \
        .filter(References.Source == request.form['Id']).distinct()

    fdata = getNeighborNetwork(int(request.form['Id']))

    return render_template('target.html', ftbooks=ftbooks, ftverses=ftverses, ftauthors=ftauthors, fdata=fdata)


@app.route('/filter_author_menu', methods=['POST'])
def filter_author_menu():

    filteredauthors = db.session.query(Sources.author, func.sum(Sources.degree).label('total')).group_by(
        Sources.author).order_by(func.sum(Sources.degree).desc()).filter_by(book=request.form['book'])

    return render_template('author_menu.html', filteredauthors=filteredauthors)