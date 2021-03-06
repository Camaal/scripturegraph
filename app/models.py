from app import db


class Books(db.Model):
    __tablename__ = "books"

    bookName = db.Column(db.String(250), nullable=False)
    testament = db.Column(db.String(2), nullable=False)
    genreName = db.Column(db.String(250), nullable=False)
    book = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Books {}>'.format(self.body)


class Authors(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(250), nullable=False)
    bookName = db.Column(db.String(250), nullable=False)
    testament = db.Column(db.String(2), nullable=False)
    genreName = db.Column(db.String(250), nullable=False)
    book = db.Column(db.Integer, primary_key=True)
    chapter = db.Column(db.Integer, nullable=False)
    degree = db.Column(db.Integer, nullable=False)
    normDegree = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return '<Authors {}>'.format(self.body)


class References(db.Model):
    __tablename__ = "cross_references"

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.Integer, db.ForeignKey('bgsource.id'))
    target = db.Column(db.Integer, db.ForeignKey('bgtarget.id'))

    def __repr__(self):
        return '<References {}>'.format(self.body)


class Sources(db.Model):
    __tablename__ = "bgsource"

    id = db.Column(db.Integer, primary_key=True)
    redLetter = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    bookName = db.Column(db.String(250), nullable=False)
    testament = db.Column(db.String(2), nullable=False)
    genreName = db.Column(db.String(250), nullable=False)
    book = db.Column(db.Integer, nullable=False)
    chapter = db.Column(db.Integer, nullable=False)
    verse = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    degree = db.Column(db.Integer, nullable=False)
    normDegree = db.Column(db.Float, nullable=True)

    targets = db.relationship('References')

    def __repr__(self):
        return '<Sources {}>'.format(self.body)


# The source scripture


class Targets(db.Model):
    __tablename__ = "bgtarget"

    id = db.Column(db.Integer, primary_key=True)
    redLetter = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    bookName = db.Column(db.String(250), nullable=False)
    testament = db.Column(db.String(2), nullable=False)
    genreName = db.Column(db.String(250), nullable=False)
    book = db.Column(db.Integer, nullable=False)
    chapter = db.Column(db.Integer, nullable=False)
    verse = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    degree = db.Column(db.Integer, nullable=False)
    normDegree = db.Column(db.Float, nullable=True)

    sources = db.relationship('References')

    def __repr__(self):
        return '<Targets {}>'.format(self.body)
