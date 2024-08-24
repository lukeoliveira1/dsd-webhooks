from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class BookServerHandler(BaseHTTPRequestHandler):
    books = [
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
        {"title": "1984", "author": "George Orwell", "year": 1949},
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
    ]

    def do_POST(self):
        print("Received POST request")
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data)
            action = data.get("action")

            if action == "add":
                self.add_book(data)
            elif action == "delete":
                self.delete_book(data)
            else:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                response = {"status": "error", "message": "Invalid action"}
                self.wfile.write(json.dumps(response).encode("utf-8"))
                print("Invalid action")
                return

        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"status": "error", "message": "Invalid JSON"}
            self.wfile.write(json.dumps(response).encode("utf-8"))
            print("Error decoding JSON")
            return

    def add_book(self, data):
        book_title = data.get("title")
        book_author = data.get("author")
        book_year = data.get("year")

        if not book_title or not book_author or not book_year:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"status": "error", "message": "Missing required fields"}
            self.wfile.write(json.dumps(response).encode("utf-8"))
            print("Missing required fields")
            return

        # adds book to the list
        self.books.append(
            {"title": book_title, "author": book_author, "year": book_year}
        )
        print("Book added successfully")

        # send successfully message
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"status": "success", "message": "Book added successfully"}
        self.wfile.write(json.dumps(response).encode("utf-8"))
        print("Book added successfully")
        return

    def delete_book(self, data):
        book_title = data.get("title")

        if not book_title:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"status": "error", "message": "Missing required fields"}
            self.wfile.write(json.dumps(response).encode("utf-8"))
            print("Missing required fields")
            return

        for book in self.books:
            if book["title"] == book_title:
                self.books.remove(book)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                response = {"status": "success", "message": "Book deleted successfully"}
                self.wfile.write(json.dumps(response).encode("utf-8"))
                print("Book deleted successfully")
                return

        self.send_response(404)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = {"status": "error", "message": "Book not found"}
        self.wfile.write(json.dumps(response).encode("utf-8"))
        print("Book not found")
        return


def run(server_class=HTTPServer, handler_class=BookServerHandler, port=5000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting book server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
