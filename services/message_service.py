# message_service.py
import os
import json
from models.message import Message
from dateutil.parser import isoparse
import math
class MessageService:
    """
    Service layer: handles business logic and JSON file persistence
    for message board, including simple pagination.
    """
    def __init__(self, json_path='data/messages.json'):
        self.json_path = json_path
        # Ensure data file exists, create directory + empty list if needed
        if not os.path.exists(self.json_path):
            os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4)

    def _read_messages(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            items = json.load(f)
        # Convert dicts back into Message instances
        return [Message.from_dict(item) for item in items]

    def _write_messages(self, messages):
        # Serialize each Message via to_dict()
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump([m.to_dict() for m in messages], f, indent=4)

    def create_message(self, data):

        if not isinstance(data, dict):
            raise ValueError("Input must be a JSON object.")

        username = data.get('username')
        message = data.get('message')

        # Field presence and length validation
        if not username:
            raise KeyError("Field 'username' is required.")
        if len(username) > 20:
            raise ValueError("Field 'username' must be at most 20 characters.")
        if not message:
            raise KeyError("Field 'message' cannot be empty.")
        if len(message) > 50:
            raise ValueError("Field 'message' must be at most 50 characters.")

        # Load existing messages to determine next ID
        messages = self._read_messages()
        next_id = max((m.id for m in messages), default=0) + 1

        # Create new Message and persist
        msg = Message(id=next_id, username=username, message=message)
        messages.append(msg)
        self._write_messages(messages)
        return msg.to_dict()

    def get_messages(self, page=1, limit=math.inf):
        messages = self._read_messages()
        # Sort by parsed ISO timestamp descending
        messages.sort(key=lambda m: isoparse(m.created_at), reverse=True)
        total = len(messages)

        # Compute slice for requested page
        start = (page - 1) * limit
        end = start + limit
        subset = messages[start:end]
        return [m.to_dict() for m in subset], total
