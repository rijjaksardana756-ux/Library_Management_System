from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simple in-memory library data for a beginner-friendly project.
books = [
    {"id": 101, "name": "Python for Everyone", "author": "A. Smith", "available": True},
    {"id": 102, "name": "Data Structures", "author": "R. Khan", "available": True},
    {"id": 103, "name": "Computer Networks", "author": "M. Rao", "available": False},
]


@app.route("/")
def home():
    """Show the home page of the library system."""
    return render_template("index.html")


@app.route("/books", methods=["GET", "POST"])
def books_page():
    """Show all books and allow adding a new book."""
    message = None

    if request.method == "POST":
        new_name = request.form.get("book_name", "").strip()
        new_author = request.form.get("author", "").strip()

        if new_name and new_author:
            new_id = max(book["id"] for book in books) + 1
            books.append({
                "id": new_id,
                "name": new_name,
                "author": new_author,
                "available": True,
            })
            message = f"Book '{new_name}' added successfully."
        else:
            message = "Please enter both the book name and author."

    return render_template("books.html", books=books, message=message)


@app.route("/books/issue/<int:book_id>", methods=["POST"])
def issue_book(book_id):
    """Mark a book as issued when the issue button is clicked."""
    for book in books:
        if book["id"] == book_id:
            if book["available"]:
                book["available"] = False
            break
    return redirect(url_for("books_page"))


@app.route("/books/return/<int:book_id>", methods=["POST"])
def return_book(book_id):
    """Mark a book as available when the return button is clicked."""
    for book in books:
        if book["id"] == book_id:
            book["available"] = True
            break
    return redirect(url_for("books_page"))


if __name__ == "__main__":
    app.run(debug=True)
