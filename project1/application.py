import os
import pandas as pd

from flask import Flask, session, render_template, request, redirect, flash, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.expression import cast
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, session, flash

from models import Book, Review
from dao import ReviewDao, BookDao

#encrypt
from passlib.hash import sha256_crypt

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

  
@app.route("/")
def index():
	login = db.execute("SELECT * FROM login2").fetchall()
	return render_template("index.html", login=login)


@app.route("/registration", methods=["POST"])
def singup():
    """Registration Request."""
    
    #Get form information.
    user_name = request.form.get("user_name_su")
    user_pass = request.form.get("user_pass_su")
    
    if not user_name or not user_pass:
        return render_template("error.html", message="SingUP #4 Invalid user name or password, please type one.")
    
    try:
        if db.execute("SELECT * FROM login2 WHERE usr_name = :user_name",
                      {"user_name": user_name}).rowcount == 1:
            flash('#5 This user is already in user, please select another.')
            return render_template("error.html", message="#5 This user is already in user, please select another.")		

        db.execute("INSERT INTO login2 (usr_name, usr_pass) VALUES (:user_name, :user_pass)",
                   {"user_name": user_name, "user_pass": user_pass})
        db.commit()

        flash('Success! You have been registrated successfully')
        return redirect('/')
        
    except ValueError:
        flash('#6 ERROR Please contact the server database')
        return render_template("error.html", message="#6 ERROR Please contact the server dba")


@app.route("/login", methods=["POST"])
def login():
    """Login Request."""  
    autenticar()



@app.route('/autenticar', methods=['POST',])
def autenticar():
    user_name = request.form.get("user_name")
    user_pass = request.form.get("user_pass")
    app.secrety_key = str(user_pass)

    if not user_name or not user_pass:
        flash('#10 Invalid password/password.')
        return redirect('/')
    
    try:
        if db.execute("SELECT * FROM login2 WHERE usr_name = :user_name",
                      {"user_name": user_name}).rowcount == 0:
            flash('#8 No such user found in our data base')
            return redirect('/')
    except ValueError:
        flash('#2 We could not find any user with this password on our database')
        return redirect('/')

    if db.execute("SELECT * FROM login2 WHERE usr_name = :user_name AND usr_pass = :user_pass",
                      {"user_name": user_name, "user_pass" : user_pass}).rowcount == 1:
        
        user_id = db.execute("SELECT usr_id FROM login2 WHERE usr_name = :user_name",
                {"user_name": user_name}).fetchone()
            
        session['user_id'] = str(user_id)
        session['user_name'] = str(user_name)

        
        if 'user_id' not in session or session['user_id'] == None:
            flash('not logged in, try again!')
            return redirect('/autenticar')
        
        return redirect('/books')
        '''render_template("books.html", user_name=user_name)'''
    else:
        flash('not logged in, try again 2!')
        return redirect('/')

@app.route('/logout')
def logout():
    session['user_id'] = None
    session['user_name'] = None
    flash('user disconnected successfully. see you later!!!')
    return redirect('/')

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

    isbn_list = db.execute("SELECT * FROM books WHERE isbn LIKE :search", 
        {"search": f"%{book_isbn}%"}).fetchall()

    size = len(isbn_list)

    if isbn_list is None:
        return render_template("error.html", message="nao carregou a lista")
    #   '%%:isbn%%' ",{"isbn": str(book_isbn)}).fetchall() 
    return render_template("list_isbn.html", isbn_list=isbn_list, size=size)

@app.route("/isbn_list/<int:book_isbn>")
def isnb(book_isbn):
    """Lists details about a single flight."""

    book = db.execute("SELECT * FROM books WHERE isbn = :isbn::varchar(10)", {"isbn": book_isbn}).fetchone()
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

    author_list = db.execute("SELECT * FROM books WHERE author LIKE :search", 
        {"search": f"%{book_author}%"}).fetchall()

    size = len(author_list)

    if author_list is None:
        return render_template("error.html", message="nao carregou a lista")
    #   '%%:isbn%%' ",{"isbn": str(book_isbn)}).fetchall() 
    return render_template("author_list.html", author_list=author_list, size=size, author=book_author )

''' SEARcH Title '''
@app.route("/search_title/")
def search_title():
    return render_template("search_title.html")

@app.route("/title_list", methods=["POST"])
def srch_title():  
    ''' search_by_title.html action '''

    book_title = request.form.get("book_title")

    title_list = db.execute("SELECT * FROM books WHERE title LIKE :search",
        {"search": f"%{book_title}%"}).fetchall()


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

    year_list = db.execute("SELECT * FROM books WHERE year LIKE :search", 
        {"search": f"%{book_year}%"}).fetchall()

    size = len(year_list)

    if year_list is None:
        return render_template("error.html", message="Year list failed. Please check it out.")
    #   '%%:isbn%%' ",{"isbn": str(book_isbn)}).fetchall() 
    return render_template("list_year.html", year_list=year_list, size=size, year=book_year)

''' BOOK PAGE '''
@app.route("/book_page/<book_isbn>")
def book_page(book_isbn):

    if 'user_id' not in session or session['user_id'] == None:
        flash('not logged in, try again!')
        return redirect('/autenticar')

    if len(str(book_isbn)) < 10:
        new_isbn = str(book_isbn).rjust(10, '0')

        Bb = db.execute("SELECT * FROM books WHERE isbn = :book_isbn", {"book_isbn": new_isbn}).fetchone()

    Bb = db.execute("SELECT * FROM books WHERE isbn = :book_isbn", {"book_isbn": book_isbn}).fetchone()

    # Make sure book exists.
    if Bb is None:
        return render_template("error.html", message=Bb)

    # Get all passengers.

    #reviews = db.execute("SELECT title FROM reviews WHERE book_isbn = :book_isbn",
    #                       {"book_isbn": book_isbn}).fetchall()
    reviews = []
    return render_template("book_page.html", book=Bb, reviews=reviews)

@app.route('/new_review/<book_isbn>/<book_name>')
def new_review(book_isbn, book_name):

    book_isbn = book_isbn
    book_name = book_name

    if 'user_id' not in session or session['user_id'] == None:
        flash('not logged in, try again!')
        return redirect('/autenticar')

    return render_template('send_review.html', book_isbn=book_isbn, book_name=book_name, review=None)


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

        review = Review(title, comment, rate, user_id, book_isbn)
        review_dao.save(review)

        flash('Success! You sent a new review')
        return redirect(url_for('index'))

    except ValueError:
        flash('#6 ERROR Please contact the server database')
        return render_template("error.html", message="#6 ERROR Please contact the server dba")




@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = jogo_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo
                           , capa_jogo=nome_imagem or 'capa_padrao.jpg')




JSON_SORT_KEYS = False


















