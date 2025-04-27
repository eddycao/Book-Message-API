# book.py
class Book:
    """
    Domain model for a Book.
    """
    def __init__(self, id, title, author, year, available=True):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        # Default availability if not provided
        self.available = available

    def to_dict(self):
        """
        Serialize Book to a dict for JSON output.
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'available': self.available
        }

    @classmethod
    def from_dict(cls, data):
        # Use data.get so missing keys return None (handled by __init__)
        return cls(
            id=data.get('id'),
            title=data.get('title'),
            author=data.get('author'),
            year=data.get('year'),
            # Fallback to True if 'available' missing
            available=data.get('available', True)
        )
