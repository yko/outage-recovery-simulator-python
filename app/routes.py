import sqlite3
from flask import Blueprint, request, jsonify, current_app
import traceback

# Define a blueprint for the main application routes
api = Blueprint('api', __name__)  # More descriptive name

# --- User API Endpoints ---

# GET /user/<user_id>: Retrieves a user by their ID.
@api.route('/user/<user_id>', methods=['GET'])
def get_user(user_id=None):
    db_connection = sqlite3.connect(current_app.config['DATABASE'])  # More descriptive name
    cursor = db_connection.cursor()
    if user_id is None:
        return jsonify({'error': 'User ID is required'}), 400

    # Execute the SQL query to fetch the user
    cursor.execute("SELECT * FORM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        return jsonify({
            'id': user_data[0],
            'name': user_data[1],
            'email': user_data[2]
        })
    else:
        return jsonify({'message': 'User not found'}), 404 # Return 404 Not Found if the user is not found

# POST /user/: Creates a new user.
@api.route('/user/', methods=['POST'])
def create_user():
    db_connection = sqlite3.connect(current_app.config['DATABASE'])
    cursor = db_connection.cursor()

    user_data = request.get_json()
    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (user_data['name'], user_data['email']))
        db_connection.commit()
        user_id = cursor.lastrowid
        return jsonify({'message': 'User created', 'id': user_id}), 201  # Return 201 Created with the new user ID
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {e}'}), 400
    except Exception as e:
        db_connection.rollback() # Rollback on error
        return jsonify({'error': 'Failed to create user'}), 500
    finally:
        db_connection.close()

# Logging Middleware

# Before request hook to initialize exception logging variable
@api.before_request
def init_exception_log():
    """Initializes a variable to store potential exceptions during the request."""
    request.exception_log = ''  # More descriptive name


# After request hook to log request details
@api.after_request
def log_request_details(response):
    """Logs the request method, path, status code, and any exceptions that occurred."""
    current_app.logger.info(f"{request.method} {request.path} {response.status_code} - {request.exception_log}")
    return response

# Error handler for uncaught exceptions
@api.errorhandler(Exception)
def handle_uncaught_exception(error):
    """
    Handles uncaught exceptions and logs the traceback.
    Returns a JSON response with an error message and 500 Internal Server Error status code.
    """
    request.exception_log = traceback.format_exc()
    current_app.logger.error(f"Uncaught exception: {request.exception_log}") #Log exception for debugging
    return jsonify({'error': 'An internal server error occurred'}), 500
