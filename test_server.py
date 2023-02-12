import requests

response = requests.put(
    'http://127.0.0.1:5000/books/1',
    json={'name': 'Hillel'})

print(response.status_code)
print(response.text)
