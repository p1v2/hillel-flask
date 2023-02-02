import requests

response = requests.delete(
    "http://127.0.0.1:5000/books/1",
    json={"name": "Book name"}
)

print(response.status_code)
print(response.json())
