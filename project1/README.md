# Project 1

Web Programming with Python and JavaScript

Requeriments for this project:

    Registration: Users should register with username and password. Please check the singup() and newuser()in Application for that
    Login: Users log in with their username and password. Please check login() and autenticar() in Application for that
    Logout: users log out . Please check logout() for that

    Import:  called books.csv with 5000 books listed (ISBN number,title, author,year).
    import.py file is in the project as well. The program imported the register into PostgreSQL database.

    Search: user has logged in, it Goes to a page where with many different ways to search for a book.
        ISBN number of a book, the title of a book, or the author of a book and Year.
        The webpp shows a list of possible matching results and some sort of message if there were no matches.
        * If the user typed in only part of a title, ISBN, or author name, your search page should find matches for those as well! *

    Book Page: users click on a book from the results of the search page, and go to book page showing
         title        >>>> search_title() and srch_title()
         author       >>>> search_author() and def srch_author()
         publication  >>>> year search_year() and srch_year()
         ISBN number  >>>> search_isbn() and srch_isbn() and isnb(book_isbn)
         reviews that users have left for the book on your website.

    Review Submission: On the book page, users should be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book. Users should not be able to submit multiple reviews for the same book.
Goodreads Review Data: On your book page, you should also display (if available) the average rating and number of ratings the work has received from Goodreads.
API Access: If users make a GET request to your website’s /api/<isbn> route, where <isbn> is an ISBN number, your website should return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON should follow the format:
