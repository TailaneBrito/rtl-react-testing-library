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

class Login:
    def __init__(self, usr_name, usr_pass, usr_id=None):
        self.usr_id = usr_id
        self.usr_name = usr_name
        self.usr_pass = usr_pass
