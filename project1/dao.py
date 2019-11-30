import os
from models import Book, Review
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, session, render_template, request, redirect, flash, url_for



SQL_CREATE_REVIEW = "INSERT into reviews (title, comment, rate, user_name, book_isbn) values (:title, :comment, :rate, :user_name, :book_isbn)"
SQL_UPDATE_REVIEW = 'UPDATE reviews SET title = :title , comment = :comment , rate= :rate, book_isbn = :book_isbn ' \
                    'WHERE id = :id'
SQL_LAST_ID = "SELECT currval('reviews_id_seq')"


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

class ReviewDao:
    def __init__(self, db):
        self.__db = db

    def save(self, review):


        if (review.id):
            try:
                # title, content, user_name, book_isbn, id=None):{"book_isbn": book_isbn}
                db.execute(SQL_UPDATE_REVIEW, {"title": review.title,
                                               "comment": review.comment,
                                               "rate": review.rate,
                                               "user_name": review.user_name,
                                               "book_isbn": review.book_isbn,
                                               "id": review.id
                                               })
            except ValueError:
                flash('Dao1 ERROR Please contact the server database')
                return render_template("error.html", message="Dao1 ERROR Please contact the server dba")
        else:
            try:
                db.execute(SQL_CREATE_REVIEW, {"title": review.title,
                                               "comment": review.comment,
                                               "rate": review.rate,
                                               "user_name": review.user_name,
                                               "book_isbn": review.book_isbn
                                               })

                review.id = db.flush()

                db.commit()
                return review

            except ValueError:
                flash('Dao2 ERROR Please contact the server database')
                return render_template("error.html", message="Dao2 ERROR Please contact the server dba")

class BookDao:
    def __init__(self, db):
        self.__db = db



