from flask import Flask, requestf
import sqlite3

from serializers import serialize_book

app = Flask(__name__)


def get_books(connection):
    cursor = connection.cursor()
    response = cursor.execute("select * from books")

    books_representation = []
    for item in response:
        books_representation.append(serialize_book(item))

    return books_representation


def create_book(connection):
    body = request.json

    book_name = body["name"]

    if book_name == "":
        return {"error": "Book name cannot be empty"}, 400

    cursor = connection.cursor()
    cursor.execute(f"insert into books (name) values ('{book_name}')")

    connection.commit()
    return {"name": book_name}, 201


@app.route("/books", methods=["GET", "POST"])
def books():
    connection = sqlite3.connect("db.sqlite")
    try:
        if request.method == "GET":
            # GET /books - list of all books
            return get_books(connection)
        elif request.method == "POST":
            # POST /books - create a book
            return create_book(connection)
    finally:
        connection.close()


def get_book(connection, book_id):
    cursor = connection.cursor()

    response = cursor.execute(f"select * from books where id={book_id}")
    book_representation = response.fetchone()

    if book_representation is None:
        return {"error": "Book not found"}, 404

    return serialize_book(book_representation)


def put_book(connection, book_id):
    body = request.json
    update_book_name = body["name"]
    if update_book_name == "":  # Checking for an empty term in the book title
        return {"error": "Book name cannot be empty"}, 400

    cursor = connection.cursor()
    response = cursor.execute(f"SELECT * FROM books WHERE id = {book_id}")
    book_representation = response.fetchone()
    if book_representation is None:  # Checking that the book with this id exists
        return {"error": "Book not found"}, 404

    cursor = connection.cursor()
    cursor.execute(f"UPDATE books SET name = '{update_book_name}' WHERE id = {book_id}")
    connection.commit()
    return {"id": book_id, "name": update_book_name}, 200


def delete_book(connection, book_id):
    cursor = connection.cursor()

    cursor.execute(f"delete from books where id={book_id}")
    connection.commit()

    # No Content
    return "", 204


@app.route("/books/<int:book_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def book(book_id):
    connection = sqlite3.connect("db.sqlite")
    if request.method == "GET":
        return get_book(connection, book_id)
    elif request.method == "PUT":
        return put_book(connection, book_id)
    elif request.method == "PATCH":
        return "book partial update will be there"
    elif request.method == "DELETE":
        return delete_book(connection, book_id)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
