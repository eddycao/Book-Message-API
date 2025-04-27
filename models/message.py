# message.py
from datetime import datetime

class Message:
    """
    Domain model for a Message in the message board.
    """
    def __init__(self, id, username, message, created_at=None):
        self.id = id
        self.username = username
        self.message = message
        # The trailing 'Z' indicates UTC time
        self.created_at = created_at or datetime.utcnow().isoformat() + 'Z'

    def to_dict(self):
        """
        Serialize Message to a dict for JSON output.
        """
        return {
            'id': self.id,
            'username': self.username,
            'message': self.message,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        # Use data.get so missing keys return None (handled by __init__)
        return cls(
            id=data.get('id'),
            username=data.get('username'),
            message=data.get('message'),
            created_at=data.get('created_at')  # preserve original timestamp if present
        )
