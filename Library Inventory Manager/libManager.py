# =================================================
#  Name = Akhil Kushwaha
#  Roll no = 2501730167
#  Course = B.tech CSE (AI/ML)
#  Section = D
# **********LIBRARY INVENTORY MANAGER************
# =================================================

import json
from pathlib import Path

# -------------------- Book Class -------------------- #
class Book:
    """Represents a book in the library"""

    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author} | ISBN: {self.isbn} | {self.status.upper()}"

    def to_dict(self):
        return vars(self)

    @classmethod
    def load(cls, data):
        return cls(data['title'], data['author'], data['isbn'], data.get('status', 'available'))

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_back(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False


# -------------------- Inventory Class -------------------- #
class Library:
    """Handles book inventory and JSON file operations"""

    def __init__(self, file="library_data.json"):
        self.file = Path(file)
        self.books = []
        self.load()

    def add(self, book):
        if any(b.isbn == book.isbn for b in self.books):
            print("Book with this ISBN already exists!")
            return False
        self.books.append(book)
        self.save()
        print("Book added successfully.")
        return True

    def find_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def find_isbn(self, isbn):
        return next((b for b in self.books if b.isbn == isbn), None)

    def find_author(self, author):
        return [b for b in self.books if author.lower() in b.author.lower()]

    def save(self):
        with open(self.file, "w") as f:
            json.dump([b.to_dict() for b in self.books], f, indent=4)

    def load(self):
        if self.file.exists():
            with open(self.file) as f:
                self.books = [Book.load(x) for x in json.load(f)]
        else:
            self.books = []

    def stats(self):
        total = len(self.books)
        available = sum(b.status == "available" for b in self.books)
        return {"total": total, "available": available, "issued": total - available}

    def show_all(self):
        if not self.books:
            print("No books available!")
            return
        print("\n===== LIBRARY BOOKS =====")
        for b in self.books:
            print("-", b)
        print("=========================")


# -------------------- User Interface Functions -------------------- #
def menu():
    print("""
========== Library Inventory ==========
1. Add Book
2. Issue Book
3. Return Book
4. Show All Books
5. Search by Title
6. Search by ISBN
7. Search by Author
8. View Statistics
9. Exit
=======================================
""")

def get_text(prompt):
    return input(prompt).strip()

def ui_add(lib):
    title = get_text("Book title: ")
    author = get_text("Author: ")
    isbn = get_text("ISBN: ")
    lib.add(Book(title, author, isbn))

def ui_issue(lib):
    isbn = get_text("ISBN to issue: ")
    book = lib.find_isbn(isbn)
    if not book:
        print("Book not found!")
    elif book.issue():
        lib.save()
        print("Book issued.")
    else:
        print("Already issued.")

def ui_return(lib):
    isbn = get_text("ISBN to return: ")
    book = lib.find_isbn(isbn)
    if not book:
        print("Book not found!")
    elif book.return_back():
        lib.save()
        print("Book returned.")
    else:
        print("Book already available.")

def ui_search_title(lib):
    title = get_text("Search title: ")
    results = lib.find_title(title)
    print("\n".join(str(b) for b in results) if results else "No results.")

def ui_search_isbn(lib):
    isbn = get_text("Search ISBN: ")
    book = lib.find_isbn(isbn)
    print(book if book else "Book not found.")

def ui_search_author(lib):
    author = get_text("Search author: ")
    results = lib.find_author(author)
    print("\n".join(str(b) for b in results) if results else "No results.")

def ui_stats(lib):
    s = lib.stats()
    print(f"Total: {s['total']} | Available: {s['available']} | Issued: {s['issued']}")


# -------------------- Main App -------------------- #
def main():
    lib = Library()

    actions = {
        "1": ui_add,
        "2": ui_issue,
        "3": ui_return,
        "4": lambda l: l.show_all(),
        "5": ui_search_title,
        "6": ui_search_isbn,
        "7": ui_search_author,
        "8": ui_stats
    }

    while True:
        menu()
        choice = get_text("Enter choice: ")

        if choice == "9":
            print("Goodbye!")
            break
        elif choice in actions:
            actions[choice](lib)
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
   
