from app import db


class Books(db.Model):
    #__tablename__ = "books"

    book_name = db.Column(db.String(250), nullable=False)
    testament = db.Column(db.String(2), nullable=False)
    genre_name = db.Column(db.String(250), nullable=False)
    book = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Books {}>'.format(self.body)


class References(db.Model):
    #__tablename__ = "references"

    Id = db.Column(db.Integer, primary_key=True)
    Source = db.Column(db.Integer, db.ForeignKey('source.Id'))
    Target = db.Column(db.Integer, db.ForeignKey('source.Id'))

    def __repr__(self):
        return '<References {}>'.format(self.body)


class Sources(db.Model):
    #__tablename__ = "source"

    Id = db.Column(db.Integer, primary_key=True)
    red_letter = db.Column(db.Boolean, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    book_name = db.Column(db.String(250), nullable=False)
    testament = db.Column(db.String(2), nullable=False)
    genre_name = db.Column(db.String(250), nullable=False)
    book = db.Column(db.Integer, nullable=False)
    chapter = db.Column(db.Integer, nullable=False)
    verse = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    degree = db.Column(db.Integer, nullable=False)

    targets = db.relationship('Sources', secondary=References, primaryjoin=(References.Source == Id),
                              secondaryjoin=(References.Target == Id), backref=db.backref('references', lazy='dynamic'))

    def __repr__(self):
        return '<Source {}>'.format(self.body)

    def cross_references(self):
        return Sources.query.join(
            References, (References.Source == Sources.Id)).filter(
            References.Target == self.Id).order_by(Sources.book.desc()
        )


# The source scripture


class Targets(db.Model):
    #__tablename__ = "target"

    Id = db.Column(db.Integer, primary_key=True)
    red_letter = db.Column(db.Boolean, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    book_name = db.Column(db.String(250), nullable=False)
    testament = db.Column(db.String(2), nullable=False)
    genre_name = db.Column(db.String(250), nullable=False)
    book = db.Column(db.Integer, nullable=False)
    chapter = db.Column(db.Integer, nullable=False)
    verse = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    degree = db.Column(db.Integer, nullable=False)

    sources = db.relationship('References')