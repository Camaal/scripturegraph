from flask import Flask, render_template, url_for, request, flash, redirect

from app import app, db
from app.models import References, Sources, Targets
from app.forms import LoginForm
from sqlalchemy import func
from pyvis.network import Network
import networkx as nx


@app.template_filter()
def numberFormat(value):
    return format(int(value), ',d')

def flat_list(l):
    return ["%s" % v for v in l]


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/bible_data')
def bible_data():
    # List all books in order they were written
    books = db.query(Sources.book_name).distinct().order_by(Sources.book)

    # Sum degree for each book
    bookDegrees = db.query(Sources.book_name, func.sum(Sources.degree).label('total')).group_by(
        Sources.book_name).order_by(Sources.book).all()

    # List all the chapters in order
    chapters = db.query(Sources.chapter).distinct().order_by(Sources.chapter)

    # Sum degree for each chapter
    chapterDegrees = db.query(Sources.chapter, func.sum(Sources.degree).label('total')).group_by(
        Sources.chapter).order_by(Sources.chapter).all()

    # List all the authors of each book and chapter
    authors = db.query(Sources.author).distinct().order_by(Sources.author)

    # Sum degree for each chapter
    authorDegrees = db.query(Sources.author, func.sum(Sources.degree).label('total')).group_by(
        Sources.author).order_by(Sources.author).all()

    # Calculate the average degree of a given book (eventually replace the book with a variable triggered by a button)
    avgdegree = db.query(func.avg(Sources.degree)).filter_by(book=1).all()

    # Calculate min degree
    mindegree = db.query(func.min(Sources.degree)).filter_by(book=1).all()

    # Calculate max degree
    maxdegree = db.query(func.max(Sources.degree)).filter_by(book=1).all()

    # List distinct chapters for a given book
    dchapters = db.query(Sources.chapter).distinct().filter_by(book=1).count()

    # List chapters, verses, and text for a given book
    dverses = db.query(Sources.chapter, Sources.verse, Sources.text, Sources.degree).filter_by(book=1)

    # List book, book name, and chapter for cross-references related to Gen 1:1
    tbooks = db.query(Targets.book, Targets.book_name, Targets.chapter, Targets.author).distinct().join(References).filter(
        References.Source == 1001001).all()

    # List book, book name, chapter, verse, text and degree for cross-references related to Gen 1:1
    joins = db.query(Targets.book_name, Targets.book, Targets.chapter, Targets.verse, Targets.text,
                          Targets.degree).join(References).filter(References.Source == 1001001).all()

    # Return a list of nodes
    nodes = flat_list(db.query(Sources.Id).filter_by(book=1, chapter=1).all())

    # Network view
    nx_graph = nx.Graph()
    nx_graph.add_nodes_from(nodes)
    # height = "500px",
    # width = "500px",
    # directed = False,
    # notebook = False,
    # bgcolor = "#ffffff",
    # font_color = False,
    # layout = None,
    # heading = ""
    nt = Network("100%", "100%", heading=" ")

    # populates the nodes and edges data structures
    nt.from_nx(nx_graph)
    p = nt.show("static/nx.html")




    # Return the data to index.html

    return render_template('index.html',
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
                           authorDegrees=authorDegrees,
                           p=p
                           )
