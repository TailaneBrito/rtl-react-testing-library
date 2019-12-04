from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Logins(db.Model):
    __tablename__ = "login2"
    usr_id = db.Column(db.Integer, primary_key=True)
    usr_name = db.Column(db.String, db.ForeignKey("reviews.user_name"), nullable=False)
    usr_pass = db.Column(db.String, nullable=False)


class Books(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, db.ForeignKey("reviews.book_isbn"), primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)


class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    book_isbn = db.Column(db.String, nullable=False)

    user_name = db.relationship("Login", backref="review", lazy=True)
    book_isbn = db.relationship("Book", backref="review", lazy=True)


