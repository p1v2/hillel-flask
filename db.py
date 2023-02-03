from peewee import *

db = SqliteDatabase("db.sqlite")

# db2 = PostgresqlDatabase(...)
# class Authors:
#     class Meta:
#         database = db2


class Author(Model):
    first_name = CharField(max_length=20)
    last_name = CharField(max_length=30)

    class Meta:
        database = db


class Book(Model):
    name = CharField(max_length=20, unique=True)
    description = TextField()
    pages_count = IntegerField()
    price = FloatField()
    author = ForeignKeyField(Author)

    class Meta:
        database = db


if __name__ == "__main__":
    # db.create_tables([Author, Book])
    books = []
    for i in range(10000):
        books.append(
            Book(name=f"Книжка {i + 1000}", description="Тест", pages_count=100, price=10, author_id=1)
        )

    Book.bulk_create(books)
