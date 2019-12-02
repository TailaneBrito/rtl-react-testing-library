'''
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Login(db.Model):
    __tablename__ = "login2"
    usr_id = db.Colum(db.Integer, primary_key=True)
    usr_name = db.Colum(db.String, nullable=False)
    usr_pass = db.Colum(db.String, nullable=False)

    def __init__(self, usr_name, usr_pass, user_id=None):
        self.user_id = user_id
        self.usr_name = usr_name
        self.usr_pass = usr_pass
'''
class Book:
    def __init__(self, title, year, author, id=None):
        self.id = id
        self.title = title
        self.author = author
        self.year = year

class Review:
    def __init__(self, title, comment, rate, user_name, book_isbn, id=None):
        self.id = id
        self.title = title
        self.comment = comment
        self.rate = rate
        self.user_name = user_name
        self.book_isbn = book_isbn
