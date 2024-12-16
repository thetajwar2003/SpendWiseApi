from flask import Blueprint, request, jsonify, current_app
from ..models.user_model import UserModel
from ..controllers.auth_controller import AuthController

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.before_request
def setup_controller():
    """
    Initialize `auth_controller` and `user_model` for every request dynamically.
    """
    global auth_controller, user_model
    user_model = UserModel(current_app.dynamodb)
    auth_controller = AuthController(
        current_app.cognito, user_model, current_app.config)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    # Input validation
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not all([email, password, first_name, last_name]):
        return jsonify({"error": "All fields (email, password, first_name, last_name) are required"}), 400

    result, status_code = auth_controller.register_user(
        email, password, first_name, last_name)
    return jsonify(result), status_code


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    # Input validation
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    result, status_code = auth_controller.login_user(email, password)
    return jsonify(result), status_code


@auth_bp.route('/sign_out', methods=['POST'])
def sign_out():
    """
    Sign out the user by invalidating their access token.
    """
    # Get the access token from the request header
    access_token = request.headers.get("Authorization")

    if not access_token:
        return jsonify({"error": "Access token is required"}), 400

    # Remove the "Bearer " prefix if present
    if access_token.startswith("Bearer "):
        access_token = access_token[len("Bearer "):]

    # No user model needed for sign out
    auth_controller = AuthController(current_app.cognito, None)
    return jsonify(*auth_controller.sign_out(access_token))
