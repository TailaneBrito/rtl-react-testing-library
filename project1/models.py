class Book:
    def __init__(self, title, year, author, id=None):
        self.id = id
        self.title = title
        self.author = author
        self.year = year

class Review:
    def __init__(self, title, content, user_name, book_isbn, id=None):
        self.id = id
        self.content = content
        self.user_name = user_name
        self.book_isbn = book_isbn
