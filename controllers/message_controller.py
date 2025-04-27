# message_controller.py
from flask import Blueprint, jsonify, request
from services.message_service import MessageService
from datetime import datetime
from math import ceil
import time

message_bp = Blueprint('messages', __name__, url_prefix='/messages')
service = MessageService()

def make_response(success, data=None, message=None, status_code=200, error_code=None, **extras):
    # Build standard response payload
    payload = {
        'success': success,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    if data is not None:
        payload['data'] = data
        # When returning a list, include pagination metadata if present
        if isinstance(data, list):
            payload['total'] = extras.get('total', len(data))
            payload['page'] = extras.get('page')
            payload['limit'] = extras.get('limit')
            if 'total_pages' in extras:
                payload['total_pages'] = extras['total_pages']
                payload['has_prev'] = extras.get('has_prev', False)
                payload['has_next'] = extras.get('has_next', False)
    # Attach error code only on failures
    if not success and error_code:
        payload['error_code'] = error_code
    if message:
        payload['message'] = message
    # Merge any other extras (excluding pagination keys already handled)
    payload.update({
        k: v for k, v in extras.items()
        if k not in ('total', 'page', 'limit', 'total_pages', 'has_prev', 'has_next')
    })
    return jsonify(payload), status_code

@message_bp.route('', methods=['POST'])
def post_message():
    # Parse JSON body without raising on failure
    payload = request.get_json(silent=True)
    if not payload or not isinstance(payload, dict):
        return make_response(False,
                             message='Request body must be a valid JSON object.',
                             status_code=400,
                             error_code='INVALID_JSON')
    try:
        # Delegate creation and validation to service layer
        msg = service.create_message(payload)
        return make_response(True,
                             data=msg,
                             message='Message posted successfully.',
                             status_code=201)
    except KeyError as e:
        # Missing required field
        return make_response(False,
                             message=str(e),
                             status_code=400,
                             error_code='VALIDATION_ERROR')
    except ValueError as e:
        # Field value invalid (e.g. too long)
        return make_response(False,
                             message=str(e),
                             status_code=400,
                             error_code='VALIDATION_ERROR')
    except Exception as e:
        # Catch-all for unexpected errors
        return make_response(False,
                             message=f"Internal server error: {e}",
                             status_code=500,
                             error_code='SERVER_ERROR')

@message_bp.route('', methods=['GET'])
def get_messages():
    # Parse and validate pagination params
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 999))
        if page < 1 or limit < 1:
            raise ValueError
    except ValueError:
        return make_response(False,
                             message='Query params page and limit must be positive integers.',
                             status_code=400,
                             error_code='INVALID_PARAMS')

    try:
        msgs, total = service.get_messages(page=page, limit=limit)
        total_pages = ceil(total / limit) if total else 1

        # Handle page out-of-range
        if page > total_pages:
            return make_response(False,
                                 data=[],
                                 message=f"Page {page} out of range. Total pages: {total_pages}.",
                                 status_code=400,
                                 error_code='OUT_OF_RANGE',
                                 total=total,
                                 page=page,
                                 limit=limit,
                                 total_pages=total_pages,
                                 has_prev=(page > 1),
                                 has_next=False)

        # Successful paginated response
        return make_response(True,
                             data=msgs,
                             status_code=200,
                             total=total,
                             page=page,
                             limit=limit,
                             total_pages=total_pages,
                             has_prev=(page > 1),
                             has_next=(page < total_pages))
    except Exception as e:
        return make_response(False,
                             message=f"Internal server error: {e}",
                             status_code=500,
                             error_code='SERVER_ERROR')
