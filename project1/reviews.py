INSERT INTO reviews (title, comment, rate, user_name, book_isbn)
VALUES ('Dreams from My Father', 'muito bom', '4', 'luan@gmail.com', '1921351438');


CREATE TABLE reviews (
    id SERIAL NOT NULL,
    title VARCHAR(50),
    comment VARCHAR(150),
    rate INTEGER NOT NULL,
    user_name VARCHAR REFERENCES login2(usr_name),
    book_isbn VARCHAR REFERENCES books(isbn),
    PRIMARY KEY (id)
)



#Examples to study later
# Bb = db.execute("SELECT * FROM books WHERE isbn = :book_isbn", {"book_isbn": {str(new_isbn)}}).fetchone()
# bd2 = db.execute("SELECT * FROM books WHERE (SELECT cast(isbn as text)) = :book_isbn ", {"book_isbn": new_isbn}).fetchone()

# db.execute("ALTER TABLE books ALTER COLUMN isbn TYPE INTEGER USING isbn::integer")
# b = db.execute("SELECT cast(isbn as text) from books where cast(isnb as text) = :book_isbn", {"book_isbn": {str(new_isbn)}}).fetchone()
