from datetime import datetime

import requests

start = datetime.now()
response = requests.get(
    "http://127.0.0.1:5001/books",
)
end = datetime.now()

print((end - start).total_seconds())
