# Project 1

Web Programming with Python and JavaScript

Requeriments for this project:

    Registration:   Users should register with username and password. Please check the singup() and
                    newuser()in Application for that
    Login:          Users log in with their username and password. Please check login() and autenticar()
                    in Application for that
    Logout:         users log out . Please check logout() for that

    Import:         called books.csv with 5000 books listed (ISBN number,title, author,year).
    import.py       file is in the project as well. The program imported the register into PostgreSQL database.

    Search:         user has logged in, it Goes to a page where with many different ways to search for a book.
                    ISBN number of a book, the title of a book, or the author of a book and Year.
                    The webpp shows a list of possible matching results and some sort of message if there were no matches.
                    * If the user typed in only part of a title, ISBN, or author name, your search page should find
                    matches for those as well! *

    Book Page:      users click on a book from the results of the search page, and go to book page showing
                     title        >>>> search_title() and srch_title()
                     author       >>>> search_author() and def srch_author()
                     publication  >>>> year search_year() and srch_year()
                     ISBN number  >>>> search_isbn() and srch_isbn() and isnb(book_isbn)
                     reviews that users have left for the book on your website.

    Review Sub:     book page, users are able to submit a review: scale of 1 to 5, title and comment for a review,
                    Users aren't able to submit multiple reviews for the same book.
    Goodreads :     book page, display the average rating and number of ratings the work has received from Goodreads.
    API Access:     /api/<book_isbn> route, where <isbn> is an ISBN number, it returns a JSON response containing
                    the book’s title, author, year, ISBN number, review count, and average score.

                                {
                                  "author": "Raymond E. Feist",
                                  "average_score": "4.32",
                                  "isbn": "0586217835",
                                  "review_count": 68118,
                                  "title": "Magician",
                                  "year": "1982"
                                }
