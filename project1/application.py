import os
import requests

from flask import Flask, session, render_template, request, redirect, flash, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import *
from dao import ReviewDao, BookDao, LoginDao

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine)) 

review_dao = ReviewDao(db)
book_dao = BookDao(db)
login_dao = LoginDao(db)

@app.route("/")
def index():
    login = login_dao.select_all_usrs()
    return render_template("index.html", login=login)

@app.route("/registration", methods=["POST"])
def singup():
    """Registration Request."""
    
    #Get form information.
    user_name = request.form.get("user_name_su")
    user_pass = request.form.get("user_pass_su")
    
    validate(user_name, user_pass)

    usr = create_user(user_name, user_pass)

    try:

        ex_login = login_dao.verify_exitence_usr(usr)

        if ex_login is None:
            return render_template("error.html",
                                   message="#5 This user is already in user, please select another.")

        login_dao.create_new_user(usr)

        flash(f'Success! You have been registrated {usr.usr_name } successfully')
        return redirect(url_for("logged",
                                user_name=usr.usr_name))
        
    except ValueError:
        flash('#6 ERROR Please contact the server database')
        return render_template("error.html",
                               message="#6 ERROR Please contact the server dba")

@app.route("/newuser")
def newuser():
    return render_template("singup.html")

@app.route("/login")
def login():
    """Login Request."""

    ln = login_dao.select_all_usrs()
    return render_template("login.html", login=ln)
    autenticar()

@app.route('/autenticar', methods=['POST',])
def autenticar():

    user_name = request.form.get("user_name")
    user_pass = request.form.get("user_pass")

    validate(user_name, user_pass)
    usr1 = create_user(user_name, user_pass)
    
    try:
        usr = login_dao.verify_exitence_usr(usr1)
        if usr is None:
            flash('#8 No such user found in our data base')
            return redirect(url_for('login'))

        id2 = login_dao.select_usr_id(usr1)

        if usr is True:
            user_section(id2, usr1.usr_name)

            return redirect(url_for('books'))
        else:
            flash('User and or Password do not match. Please try again')
            return redirect(url_for('login'))

    except ValueError:
        flash('#2 We could not find any user with this password on our database')
        return redirect('/')

@app.route('/logged/<user_name>')
def logged(user_name):
    return render_template("logged.html", user_name=user_name)


@app.route('/logout')
def logout():
    user_section(None, None)

    flash('user disconnected successfully. see you later!!!')
    return redirect('/')

@app.route('/list_reviews')
def list_reviews():
    if validate_user_section2() is not None:
        flash(session['user_name'])
        r_list = review_list(session['user_name'])
        size = len(r_list)
        return render_template("list_reviews.html", size=size, user=session['user_name'], review_list=r_list)
    else:
        return render_template("error.html", message="Something wrong")


@app.route("/books")
def books():
    """Lists all books"""
    #books = db.execute("SELECT * FROM books").fetchall()
    return render_template("books_list.html")

''' SEARcH ISBN '''
@app.route("/search_isbn/")
def search_isbn():
    return render_template("search.html")

@app.route("/isbn_list", methods=["POST"])
def srch_isbn():  
    ''' search.html action '''

    book_isbn = request.form.get("book_isbn")

    isbn_list = book_dao.select_books_isbn(book_isbn)

    size = len(isbn_list)

    if isbn_list is None:
        return render_template("error.html", message="nao carregou a lista")
    return render_template("list_isbn.html", isbn_list=isbn_list, size=size)

@app.route("/isbn_list/<int:book_isbn>")
def isnb(book_isbn):
    """Return search_isbn with a list of isbn after search."""

    book = book_dao.select_isbn_book(book_isbn)

    if book is None:
        return render_template("error.html", message="ISBN list failed. Please check it out.")

    return render_template("search_isbn.html", book=book)

''' SEARcH AUTHOR '''
@app.route("/search_author/")
def search_author():
    return render_template("search_author.html")

@app.route("/author_list", methods=["POST"])
def srch_author():  
    ''' search_by_author.html action '''

    book_author = request.form.get("book_author")

    author_list = book_dao.select_book_author(book_author)

    size = len(author_list)

    if author_list is None:
        return render_template("error.html", message="nao carregou a lista")
    return render_template("list_author.html", author_list=author_list, size=size, author=book_author )

''' SEARcH Title '''
@app.route("/search_title/")
def search_title():
    return render_template("search_title.html")

@app.route("/title_list", methods=["POST"])
def srch_title():  
    ''' search_by_title.html action '''

    book_title = request.form.get("book_title")

    title_list = book_dao.select_book_title(book_title)

    if title_list is None:
        return render_template("error.html", message="srch_title() title list failed. Please check it out.")

    return render_template("list_title.html", title_list=title_list, title=book_title)

''' SEARcH Year '''
@app.route("/search_year/")
def search_year():
    return render_template("search_year.html")

@app.route("/year_list", methods=["POST"])
def srch_year():  
    ''' search_by_year.html action '''

    book_year = request.form.get("book_year")

    year_list = book_dao.select_book_year(book_year)

    size = len(year_list)

    if year_list is None:
        return render_template("error.html", message="Year list failed. Please check it out.")

    return render_template("list_year.html", year_list=year_list, size=size, year=book_year)

''' BOOK PAGE '''
@app.route("/book_page/<book_isbn>")
def book_page(book_isbn):

    validate_user_section2()


    Bb = book_dao.select_all_books_isbn(book_isbn)

     # Make sure book exists.
    if Bb is None:
        return render_template("error.html", message=Bb)

    reviews = review_dao.selec_all_reviews_isbn(book_isbn)

    rate = search_rate_google_reads(book_isbn)

    return render_template("book_page.html", book=Bb, reviews=reviews, google_rating=rate)

@app.route('/new_review/<book_isbn>/<book_name>')
def new_review(book_isbn, book_name):

    book_isbn = book_isbn
    book_name = book_name

    review_dao.check_book_review_existence(book_isbn, book_isbn)

    if 'user_id' not in session or session['user_id'] == None:
        flash('not logged in, try again!')
        return redirect('/autenticar')

    return render_template('send_review.html',
                           book_isbn=book_isbn,
                           book_name=book_name,
                           review=None)

@app.route('/create/<book_isbn>', methods=['POST',])
def create(book_isbn):

    if 'user_id' not in session or session['user_id'] == None:
        return render_template("error.html", message="Create #4 Invalid user name or password, please type one.")
    try:

        title = request.form['title']
        comment = request.form['comment']
        user_id = session['user_name']
        rate = request.form['rate']
        book_isbn = book_isbn

        check_review_existence = review_dao.check_book_review_existence(book_isbn,user_id)
        check_lenght = (len(check_review_existence))
        print(check_lenght)

        if check_lenght >= 1:
            return render_template("error.html", message="Book already have a review by you")

        else:
            print('entrou aqui = 0')
            review = Review(title, comment, rate, user_id, book_isbn)
            review_dao.save(review)

            flash('Success! You sent a new review')
            return redirect(url_for('books'))

    except ValueError:
        flash('#6 ERROR Please contact the server database')
        return render_template("error.html", message="#6 ERROR Please contact the server dba")

def create_user(user_name, user_pass):
    lg = Login(user_name, user_pass)

    return lg

def validate(user_name, user_pass):

    if not user_name or not user_pass:
        return render_template("error.html", message="Invalid user name or password, please type one.")

def user_section(user_id, user_name):
    ''' definies the name for the session user'''
    session['user_id'] = str(user_id)
    session['user_name'] = str(user_name)

    return validate_user_section()

def validate_user_section():
    ''' Validates if a user is into the session, if not rises up an error '''

    if 'user_id' not in session or session['user_id'] or session['user_name'] == None:
        return render_template("error.html", message="Create #4 Invalid user name or password, please type one.")
    else:
        return url_for("logged", user_name=session['user_name'])

def validate_user_section2():
    if 'user_name' not in session or session['user_name'] \
            or 'user_id' not in session or session['user_id'] == None:
        return render_template("error.html",
                               message="You should log in to see this page")
def review_list(user_name):
    user_name = user_name

    reviews = db.execute("SELECT * FROM reviews WHERE user_name = :user_name",
                         {"user_name": user_name}).fetchall()

    return reviews

def search_rate_google_reads(books_isbn):
    key = "ILwXvguynynBDzXQmVmUQ"
    isbn = books_isbn
    url = "https://www.goodreads.com/book/review_counts.json"

    res = requests.get(url,
                       params={"key": key,
                               "isbns": isbn},
                       verify=False
                       )

    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    data = res.json()
    book_rating = data["books"][0]["average_rating"]
    # rate = book_rating[0]["average_rating"]

    return book_rating



JSON_SORT_KEYS = False


















