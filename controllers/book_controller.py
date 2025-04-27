# book_controller.py
from flask import Blueprint, jsonify, request
from services.book_service import BookService
from datetime import datetime
import logging

book_bp = Blueprint('books', __name__, url_prefix='/books')
service = BookService()

def make_response(success, data=None, message=None, status_code=200, error_code=None, headers=None, **extras):
    payload = {
        'success': success,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    if data is not None:
        payload['data'] = data
        if isinstance(data, list):
            # Include count for list responses
            payload['total'] = len(data)
    if not success and error_code:
        payload['error_code'] = error_code
    if message:
        payload['message'] = message
    payload.update(extras)
    # Support custom headers (e.g., Location after creation)
    if headers:
        return jsonify(payload), status_code, headers
    return jsonify(payload), status_code

@book_bp.route('', methods=['GET'])
def get_books():
    books = service.get_all_books()
    if not books:
        return make_response(True, data=books, message='No books available.', status_code=200)
    return make_response(True, data=books, status_code=200)

@book_bp.route('', methods=['POST'])
def add_book():
    payload = request.get_json(silent=True)
    if payload is None:
        return make_response(False,
                             message='Request body must be valid JSON.',
                             status_code=400,
                             error_code='INVALID_JSON')

    # Bulk create when payload is a list
    if isinstance(payload, list):
        try:
            created = service.create_books(payload)
            return make_response(
                True,
                data=created,
                message=f'{len(created)} books created successfully.',
                status_code=201
            )
        except KeyError as e:
            logging.exception(e)
            return make_response(False, message=str(e), status_code=400, error_code='VALIDATION_ERROR')
        except ValueError as e:
            logging.exception(e)
            return make_response(False, message=str(e), status_code=400, error_code='VALIDATION_ERROR')
        except Exception as e:
            logging.exception(e)
            return make_response(False, message='Internal server error', status_code=500, error_code='SERVER_ERROR')

    # Single create when payload is a dict
    if not isinstance(payload, dict):
        return make_response(False,
                             message='Request body must be a JSON object or list.',
                             status_code=400,
                             error_code='INVALID_JSON')

    try:
        book = service.create_book(payload)
        # Return Location header pointing to the new resource
        location = {'Location': f"{request.url.rstrip('/')}/{book['id']}"}
        return make_response(
            True,
            data=book,
            message='Book created successfully.',
            status_code=201,
            headers=location
        )
    except KeyError as e:
        logging.exception(e)
        return make_response(False, message=str(e), status_code=400, error_code='VALIDATION_ERROR')
    except ValueError as e:
        logging.exception(e)
        return make_response(False, message=str(e), status_code=400, error_code='VALIDATION_ERROR')
    except Exception as e:
        logging.exception(e)
        return make_response(False, message='Internal server error', status_code=500, error_code='SERVER_ERROR')

@book_bp.route('/id=<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        book = service.get_book_by_id(book_id)
        if not book:
            return make_response(False,
                                 message=f'Book with id={book_id} not found.',
                                 status_code=404,
                                 error_code='NOT_FOUND')
        return make_response(True, data=book, status_code=200)
    except Exception as e:
        logging.exception(e)
        return make_response(False, message='Internal server error', status_code=500, error_code='SERVER_ERROR')

@book_bp.route('/id=<int:book_id>', methods=['PUT'])
def update_book(book_id):
    payload = request.get_json(silent=True)
    if payload is None or not isinstance(payload, dict):
        return make_response(False,
                             message='Request body must be a JSON object.',
                             status_code=400,
                             error_code='INVALID_JSON')

    try:
        updated = service.update_book(book_id, payload)
        if not updated:
            return make_response(False,
                                 message=f'Book with id={book_id} not found.',
                                 status_code=404,
                                 error_code='NOT_FOUND')
        return make_response(True,
                             data=updated,
                             message='Book updated successfully.',
                             status_code=200)
    except Exception as e:
        logging.exception(e)
        return make_response(False, message='Internal server error', status_code=500, error_code='SERVER_ERROR')

@book_bp.route('/id=<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        ok = service.delete_book(book_id)
        if not ok:
            return make_response(False,
                                 message=f'Book with id={book_id} not found.',
                                 status_code=404,
                                 error_code='NOT_FOUND')
        return make_response(True,
                             message='Book deleted successfully.',
                             status_code=200)
    except Exception as e:
        logging.exception(e)
        return make_response(False, message='Internal server error', status_code=500, error_code='SERVER_ERROR')
