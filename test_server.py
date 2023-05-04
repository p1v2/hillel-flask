import requests

response = requests.put(
    "http://127.0.0.1:5000/books/2",
    json={"name": "London"}
)

print(response.status_code)
print(response.text)
