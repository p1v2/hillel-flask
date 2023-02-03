def serialize_book(book):
    return {
        "id": book.id,
        "name": book.name,
        "author_id": book.author_id,
        "author": {
            "first_name": book.author.first_name,
            "last_name": book.author.last_name,
        }
    }
