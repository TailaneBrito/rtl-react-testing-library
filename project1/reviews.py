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

#EXAMPLES OF QUERIES

Flight.query.filter_by(id=28).first()


flight = Flight.query.get(28)
db.session.delete(flight)
db.session.commit() #deleting, updating.

#order by
Flight.query.order_by(Flight.origin).all()
#order by descending
Flight.query.order_by(Flight.origin.desc()).all()

#Select all fights different from Paris
Flight.query.filter(Flight.origin != "Paris").all()

#Select like
Flight.query.filter(Flight.origin.like("%a%")).all()

Flight.query.filter(Flight.origin.in_(["Tokyo", "Paris"])).all()

#AND  OR
Flight.query.filter(and_(Flight.origin == "Paris",
                         Flight.duration > 500)).all()

Flight.query.filter(or_(Flight.origin == "Paris",
                         Flight.duration > 500)).all()

#JOING MULTIPLE TABLES TOGETHER
db.session.query(Flight, Passenger).filter(
    Flight.id == Passenger.flight_id).all()




SELECT * FROM reviews WHERE user_name = 'luan@gmail.com';


#Examples to study later
# Bb = db.execute("SELECT * FROM books WHERE isbn = :book_isbn", {"book_isbn": {str(new_isbn)}}).fetchone()
# bd2 = db.execute("SELECT * FROM books WHERE (SELECT cast(isbn as text)) = :book_isbn ", {"book_isbn": new_isbn}).fetchone()

# db.execute("ALTER TABLE books ALTER COLUMN isbn TYPE INTEGER USING isbn::integer")
# b = db.execute("SELECT cast(isbn as text) from books where cast(isnb as text) = :book_isbn", {"book_isbn": {str(new_isbn)}}).fetchone()
