import requests

response = requests.put(
    "http://127.0.0.1:5000/books",
    json={"id": 2, "name": "The Wee"}
)

print(response.status_code)
print(response.text)
