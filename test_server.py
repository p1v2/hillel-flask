import requests

# response = requests.post(
#     "http://127.0.0.1:5000/books",
#     json={"name": "qwerty"}
# )


response = requests.put(
    "http://127.0.0.1:5000/books/2",
    json={"name": "new_book_Author_Siromakha_Vasyl"}
)

print(response.status_code)
print(response.text)
