import requests

response = requests.put(
    "http://127.0.0.1:5001/books/8",
    json={"name": "Dragons"}
)

print(response.status_code)
print(response.text)
