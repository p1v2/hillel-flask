from flask import Flask, request
import sqlite3

from serializers import serialize_book

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def put_update_book(connection, book_id):
    body = request.json
    new_book_name = body["name"]
    cursor = connection.cursor()

    # Check updating book in the db
    response = cursor.execute(f'select name from books where id = {book_id}')
    check_book = response.fetchone()
    if not check_book:
        return {"error": "Updating book does not exist"}, 400

    # Check the book name
    elif new_book_name == "":
        return {"error": "Book name cannot be empty"}, 400

    # Update query execute
    cursor.execute(
        f"""update books
        set name = '{new_book_name}'
        where id = {book_id}
        """
    )

    connection.commit()
    return "OK", 200


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
    return "OK"


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
        return put_update_book(connection, book_id)
    elif request.method == "PATCH":
        return "book partial update will be there"
    elif request.method == "DELETE":
        return delete_book(connection, book_id)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
