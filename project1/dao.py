import os
from models import Book, Review
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, session, render_template, request, redirect, flash, url_for

#LOGIN2
db = "login2"
SQL_SELECT_ALL_LOGIN = f"SELECT * FROM { db }"
SQL_SELECT_USR_NAME = f"SELECT * FROM { db } WHERE usr_name = :user_name"
SQL_CREATE_NEW_USER = f"INSERT INTO { db } (usr_name, usr_pass) VALUES (:user_name, :user_pass)"
SQL_SELECT_USR_PSS = f"SELECT * FROM { db } WHERE usr_name = :user_name AND usr_pass = :user_pass"
SQL_SELECT_ID = f"SELECT usr_id FROM { db } WHERE usr_name = :user_name AND usr_pass = :user_pass"

#BOOKS
db2 = "books"
SQL_SELECT_BOOKS_ISBN = f"SELECT * FROM { db2 } WHERE isbn LIKE :search"
SQL_SELECT_ISBN_BOOK = f"SELECT * FROM { db2 } WHERE isbn = :isbn::varchar(10)"
SQL_SELECT_BOOKS_AUTHOR = f"SELECT * FROM { db2 } WHERE author LIKE :search"
SQL_SELECT_BOOK_TITLE = f"SELECT * FROM { db2 } WHERE title LIKE :search"
SQL_SELECT_BOOK_YEAR = f"SELECT * FROM { db2 } WHERE year LIKE :search"
SQL_ALL_BOOKS_ISBN = f"SELECT * FROM { db2 } WHERE isbn = :book_isbn"
SQL_SELECT_ALL_BOOKS = f"SELECT * FROM { db2 }"

#REVIEWS
db3 = "reviews"
SQL_CREATE_REVIEW = "INSERT into reviews (title, comment, rate, user_name, book_isbn) values (:title, :comment, :rate, :user_name, :book_isbn)"
SQL_UPDATE_REVIEW = 'UPDATE reviews SET title = :title , comment = :comment , rate= :rate, book_isbn = :book_isbn ' \
                    'WHERE id = :id'
SQL_LAST_ID = "SELECT currval('reviews_id_seq')"
SQL_CHECK_BOOK_EXIST = "SELECT book_isbn FROM reviews WHERE user_name = :user_name AND book_isbn = :book_isbn"
SQL_ALL_REVIEWS_ISBN = f"SELECT * FROM { db3 } WHERE book_isbn = :book_isbn"


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

        #if review.id already exists
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
                flash('DAO1 error while inserting values on the table.')
                return render_template("error.html", message="Dao1 REVIEW ERROR Please contact the server dba")
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
                flash('DAO2 ERROR while creating a new review')
                return render_template("error.html", message="Dao2 REVIEW ERROR Please contact the server dba")

    def check_book_review_existence(self, book_isbn, user_name):

        book_isbn = book_isbn
        user_name = user_name

        check_book_isbn_exist = db.execute((SQL_CHECK_BOOK_EXIST),
                                           {"book_isbn": book_isbn, "user_name": user_name}).fetchall()

        return check_book_isbn_exist

    def selec_all_reviews_isbn(self, book_isbn):
        try:

            isbn_list = db.execute(SQL_ALL_REVIEWS_ISBN,
                              {"book_isbn": book_isbn}).fetchall()
            return isbn_list

        except ValueError:
            return render_template("error.html", message="DAO3 REVIEW Not possible to find any review for this isbn")


class BookDao:
    def __init__(self, db):
        self.__db = db

    def select_all_books(self):
        try:
            books = db.execute(SQL_SELECT_ALL_BOOKS).fetchall()
            return books

        except ValueError:
            return render_template("error.html", message="DAO1 BOOKS Not possible to load all the books")

    def select_books_isbn(self, book_isbn):
        ''' Return all ISBN that matches the search'''
        book_isbn = book_isbn
        try:
            books = db.execute(SQL_SELECT_BOOKS_ISBN,
                              {"search": f"%{book_isbn}%"}).fetchall()
            return books

        except ValueError:
            return render_template("error.html", message="DAO2 BOOKS Not possible find books with this isbn")

    def select_isbn_book(self, book_isbn):
        ''' Return only one ISBN '''
        try:
            isbn_varchar = db.execute(SQL_SELECT_ISBN_BOOK,
                                      {"isbn": book_isbn}).fetchone()
            return isbn_varchar
        except ValueError:
            return render_template("error.html", message="DAO3 BOOKS Not possible to find book with this specific isbn")

    def select_book_author(self, book_author):
        try:
            author = db.execute(SQL_SELECT_BOOKS_AUTHOR,
                                {"search": f"%{book_author}%"}).fetchall()
            return author
        except ValueError:
            return render_template("error.html", message="DAO4 BOOKS Not possible to find book with this author")

    def select_book_title(self, book_title):
        try:
            title = db.execute(SQL_SELECT_BOOK_TITLE,
                               {"search": f"%{book_title}%"}).fetchall()
            return title
        except ValueError:
            return render_template("error.html", message="DAO5 BOOKS Not possible to find book with this title")

    def select_book_year(self, book_year):
        try:

            year = db.execute(SQL_SELECT_BOOK_YEAR,
                              {"search": f"%{book_year}%"}).fetchall()

            return year
        except ValueError:
            return render_template("error.html", message="DAO6 BOOKS Not possible to find book with this year")

    def select_all_books_isbn(self, book_isbn):

        try:
            books = db.execute(SQL_ALL_BOOKS_ISBN,
                                   {"book_isbn": book_isbn}).fetchone()

            return books
        except ValueError:
            return render_template("error.html", message="DAO5 BOOKS Not possible to find that specific book by its ibsn")


class LoginDao:
    def __init__(self, db):
        self.__db = db

    def select_all_usrs(self):
        ''' Verifies if user exists '''
        try:


            login = db.execute(SQL_SELECT_ALL_LOGIN).fetchall()
            return login

        except ValueError:
            return render_template("error.html", message="DAO3 Not possible to load all users")

    def verify_exitence_usr(self, login):
        ''' return a valid user '''

        try:

            usr = db.execute(SQL_SELECT_USR_NAME,
                             {"user_name": login.usr_name}).rowcount == 1
            return usr

        except ValueError:
            return render_template("error.html",
                                   message=f"DAO4 Not possible to find user { login.user_name }")

    def create_new_user(self, login):
        ''' Creates a new user inside into login2'''
        try:

            usr = db.execute(SQL_CREATE_NEW_USER,
                              {"user_name": login.usr_name,
                               "user_pass": login.usr_pass})
            db.commit()
            return usr

        except ValueError:
            return render_template("error.html",
                                   message=f"DAO5 Not possible to create {login.user_name}")


    def select_usr_pss(self, login):
        try:
            usr = db.execute(SQL_SELECT_USR_PSS,
                             {"user_name": login.usr_name,
                              "user_pass": login.usr_pass})


            return usr

        except ValueError:
            return render_template("error.html",
                                   message=f"DAO6 Couldn't locate {login.user_name}")

    def select_usr_id(self, login):
        try:
            id = db.execute(SQL_SELECT_ID,
                            {"user_name": login.usr_name,
                             "user_pass": login.usr_pass})
            return id

        except ValueError:
            return render_template("error.html",
                                   message=f"DAO7 Couldn't locate {login.user_name}")




