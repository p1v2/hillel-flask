import json

from flask import Flask

app = Flask(__name__)


@app.route("/books/<int:book_id>")
def books(book_id):
    if book_id < 1:
        return {"error": "Invalid book id"}, 400
    return json.dumps({"id": book_id, "name": "Кобзар"})


@app.route("/")
def hello_world():
    return f"Hello world"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
