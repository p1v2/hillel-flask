import requests

response = requests.put(
    "http://127.0.0.1:5000/books/1",
    json={"name": "Біблія"}
)

print(response.status_code)
print(response.text)
