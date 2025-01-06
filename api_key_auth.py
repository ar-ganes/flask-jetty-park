from flask import request, jsonify
from functools import wraps
from config import Config

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Extract the API key from the request headers
        api_key = request.headers.get('x-api-key')
        if not api_key or api_key != Config.API_KEY:
            return jsonify({"message": "Forbidden: Invalid or missing API key"}), 403
        return f(*args, **kwargs)
    return decorated_function
