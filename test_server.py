import requests


response = requests.put(
    "http://127.0.0.1:5001/books/3",
    json={"name": "Harry P13"}
)

print(response.status_code)
print(response.text)
