# book_service.py
import os
import json
from models.book import Book

class BookService:
    """
    Service layer: handles business logic and JSON file persistence,
    including single and bulk book creation.
    """
    def __init__(self, json_path='data/books.json'):
        self.json_path = json_path
        # Ensure storage file exists; create directory and empty list if needed
        if not os.path.exists(self.json_path):
            os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4)

    def _read_books(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            items = json.load(f)
        # Convert each dict to a Book instance
        return [Book.from_dict(item) for item in items]

    def _write_books(self, books):
        with open(self.json_path, 'w', encoding='utf-8') as f:
            # Serialize each Book via to_dict()
            json.dump([book.to_dict() for book in books], f, indent=4)

    def get_all_books(self):
        return [book.to_dict() for book in self._read_books()]

    def create_book(self, data):
        """
        Create a single book. 'data' must be a dict with required keys.
        """
        if not isinstance(data, dict):
            raise ValueError("Input must be a JSON object.")
        # Validate presence of required fields
        for field in ('title', 'author', 'year'):
            if field not in data:
                raise KeyError(f"Missing required field: {field}")

        books = self._read_books()
        # Assign next sequential ID
        new_id = max((book.id for book in books), default=0) + 1
        book = Book(
            id=new_id,
            title=data['title'],
            author=data['author'],
            year=data['year'],
            available=data.get('available', True)
        )
        books.append(book)
        self._write_books(books)
        return book.to_dict()

    def create_books(self, data_list):
        """
        Bulk create multiple books.
        'data_list' must be a list of dicts, each with required keys.
        Returns a list of created book dicts.
        """
        if not isinstance(data_list, list) or not data_list:
            raise ValueError("Input must be a non-empty list of book objects.")

        books = self._read_books()
        next_id = max((book.id for book in books), default=0) + 1
        created = []

        for idx, item in enumerate(data_list, start=1):
            if not isinstance(item, dict):
                raise ValueError(f"Item #{idx} is not a JSON object.")
            # Check for any missing required fields in this item
            missing = [f for f in ('title', 'author', 'year') if f not in item]
            if missing:
                raise KeyError(f"Item #{idx} missing fields: {', '.join(missing)}")

            book = Book(
                id=next_id,
                title=item['title'],
                author=item['author'],
                year=item['year'],
                available=item.get('available', True)
            )
            books.append(book)
            created.append(book.to_dict())
            next_id += 1

        self._write_books(books)
        return created

    def get_book_by_id(self, book_id):
        for book in self._read_books():
            if book.id == book_id:
                return book.to_dict()
        return None

    def update_book(self, book_id, data):
        books = self._read_books()
        for idx, book in enumerate(books):
            if book.id == book_id:
                # Update only provided fields
                book.title = data.get('title', book.title)
                book.author = data.get('author', book.author)
                book.year = data.get('year', book.year)
                book.available = data.get('available', book.available)
                books[idx] = book
                self._write_books(books)
                return book.to_dict()
        return None

    def delete_book(self, book_id):
        books = self._read_books()
        filtered = [book for book in books if book.id != book_id]
        # Return False if no book was removed
        if len(filtered) == len(books):
            return False
        self._write_books(filtered)
        return True
