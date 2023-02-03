import requests

response = requests.put(
    "http://127.0.0.1:5020/books/3",
    json= {'name': 'Last_book_test'}
)

print(response.status_code)
print(response.text)
