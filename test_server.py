import requests

response = requests.put(
    "http://127.0.0.1:5020/books/1",
    json= {'name': 'New_Book_Shevchenko'}
)

print(response.status_code)
print(response.text)
