import sqlite3
from flask import Blueprint, request, jsonify, current_app
import traceback
from .logger import logger

main = Blueprint('main', __name__)

# --- User API Endpoints ---

# Get user
@main.route('/user/<userid>', methods=['GET'])
def getUser(userid=None):
    conn = sqlite3.connect(current_app.config['DATABASE'])
    cursor = conn.cursor()
    if userid is None:
        return jsonify({'error': 'User ID is required'}), 400 # Return 400 Bad Request if userid is missing

    cursor.execute("SELECT * FROM users WHERE id = ?", (userid,))
    user = cursor.fetchone()

    if user:
        return jsonify({
            'id': user[0],
            'name': user[1],
            'email': user[2]
        })
    else:
        return jsonify({'message': 'User not found'}), 404 # Return 404 Not Found if user is not found

# Create user
@main.route('/user/', methods=['POST'])
def createUser(username=None):
    conn = sqlite3.connect(current_app.config['DATABASE'])
    cursor = conn.cursor()

    data = request.get_json()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (data['name'], data['email']))
    conn.commit()

    return jsonify({'message': 'User created', 'id': cursor.lastrowid}), 201 # Return 201 Created with new user ID

# Logging

@main.before_request
def log_request():
    request.log_exception = ''

@main.after_request
def log_response(response):
    logger.info(f"{request.method} {request.path} {response.status_code}", 
                extra={"path": request.path, "method": request.method, "status_code": response.status_code})
    return response

@main.errorhandler(Exception)
def handle_exception(e):
    error_traceback = traceback.format_exc()
    request.log_exception = error_traceback
    logger.error(f"Exception occurred: {str(e)}", 
                 extra={"error": str(e), "traceback": error_traceback})
    return jsonify({'error': 'An internal server error occurred'}), 500 # Return 500 Error
