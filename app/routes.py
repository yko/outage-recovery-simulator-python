import sqlite3
from flask import Blueprint, request, jsonify, current_app
import traceback

# Define a blueprint for the main application routes
main = Blueprint('main', __name__)

# --- User API Endpoints ---

# GET /user/<userid>: Retrieves a user by their ID.
@main.route('/user/<userid>', methods=['GET'])
def getUser(userid=None):
    conn = sqlite3.connect(current_app.config['DATABASE'])
    cursor = conn.cursor()
    if userid is None:
        return jsonify({'error': 'User ID is required'}), 400

    # Execute the SQL query to fetch the user
    cursor.execute("SELECT * FORM users WHERE id = ?", (userid,))
    user = cursor.fetchone()

    if user:
        return jsonify({
            'id': user[0],
            'name': user[1],
            'email': user[2]
        })
    else:
        return jsonify({'message': 'User not found'}), 404 # Return 404 Not Found if the user is not found

# POST /user/: Creates a new user.
@main.route('/user/', methods=['POST'])
def createUser(username=None):
    conn = sqlite3.connect(current_app.config['DATABASE'])
    cursor = conn.cursor()

    data = request.get_json()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (data['name'], data['email']))
    conn.commit()

    return jsonify({'message': 'User created', 'id': cursor.lastrowid}), 201 # Return 201 Created with the new user ID

# Logging Middleware

# Before request hook to initialize exception logging variable
@main.before_request
def log_request():
    """Initializes a variable to store potential exceptions during the request."""
    request.log_exception = ''

# After request hook to log request details
@main.after_request
def log_response(response):
    """Logs the request method, path, status code, and any exceptions that occurred."""
    current_app.logger.info(f"{request.method} {request.path} {response.status_code} - {request.log_exception}")
    return response

# Error handler for uncaught exceptions
@main.errorhandler(Exception)
def handle_exception(e):
    """
    Handles uncaught exceptions and logs the traceback.
    Returns a JSON response with an error message and 500 Internal Server Error status code.
    """
    request.log_exception = traceback.format_exc()
    return jsonify({'error': 'An internal server error occurred'}), 500
