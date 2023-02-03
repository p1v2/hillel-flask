import peewee
from flask import Flask, request
import urllib.parse

from db import Book, Author
from serializers import serialize_book

import logging

app = Flask(__name__)

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def get_books():
    query_string = request.args.to_dict()

    books = Book.select(Book, Author).join(Author, on=(Book.author_id == Author.id))
    # select id, name, author.first_name from book join author on book.author_id = author.id

    if "name" in query_string:
        books = books.where(Book.name == query_string["name"])
    if "author" in query_string:
        books = books.where(Author.last_name == query_string["author"])
    # where book.name = 'Кобзар'

    books_representation = []
    for book in books:
        books_representation.append(serialize_book(book))

    return books_representation


def create_book():
    body = request.json

    try:
        name = body["name"]
        description = body["description"]
        pages_count = body["pages_count"]
        price = body["price"]
        author_id = body["author_id"]
    except KeyError as error:
        missing_field = str(error)
        return {"error": f"{missing_field} is required."}, 400

    try:
        book = Book.create(name=name, description=description, pages_count=pages_count,
                           price=price, author_id=author_id)
    except peewee.IntegrityError as error:
        if "UNIQUE" in str(error):
            error_text = "field is not unique."
        else:
            error_text = str(error)
        return {"error": error_text}, 400

    # HTTP 201 - created
    return serialize_book(book), 201


@app.route("/books", methods=["GET", "POST"])
def books_endpoint():
    if request.method == "GET":
        # GET /books - list of all books
        return get_books()
    elif request.method == "POST":
        # POST /books - create a book
        return create_book()


def get_book(book_id):
    book = Book.get(id=book_id)

    if book is None:
        return {"error": "Book not found"}, 404

    return serialize_book(book)


def delete_book(book_id):
    Book.delete().where(Book.id == book_id).execute()

    # No Content
    return "", 204


@app.route("/books/<int:book_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def book_endpoint(book_id):
    if request.method == "GET":
        return get_book(book_id)
    elif request.method == "PUT":
        return "book update will be there"
    elif request.method == "PATCH":
        return "book partial update will be there"
    elif request.method == "DELETE":
        return delete_book(book_id)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
