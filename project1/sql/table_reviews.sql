CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    content VARCHAR(150) NOT NULL,
    user_name VARCHAR REFERENCES login2(usr_name),
    book_isbn VARCHAR(10) REFERENCES books(isbn)
);

INSERT INTO reviews (title, content, user_name, book_isbn) VALUES ('Great!', 'I loved that book and i would recommend it for everyone', 'tatamor@gmail.com', '0571242448');


SELECT origin, destination, name FROM flights INNER JOIN passengers ON passengers.flight_id = flights.id;
SELECT origin, destination, name FROM flights JOIN passengers ON passengers.flight_id = flights.id;
SELECT origin, destination, name FROM flights LEFT OUTER JOIN passengers ON passengers.flight_id = flights.id;
SELECT origin, destination, name FROM flights RIGHT OUTER JOIN passengers ON passengers.flight_id = flights.id;
