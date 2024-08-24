import requests
import json


def send_book(title, author, year):
    url = "http://localhost:5000/"
    headers = {"Content-Type": "application/json"}
    payload = {"title": title, "author": author, "year": year}

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("Book sent successfully", response.json())
    else:
        print("Error sending book", response.status_code, response.text)


if __name__ == "__main__":
    send_book("The Pragmatic Programmer", "Andrew Hunt, David Thomas", 1999)
