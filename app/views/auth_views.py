from flask import Blueprint, request, jsonify, current_app
from ..models.user_model import UserModel
from ..controllers.auth_controller import AuthController

auth_bp = Blueprint('auth_bp', __name__)
user_model = UserModel(current_app.dynamodb)
auth_controller = AuthController(current_app.cognito, user_model)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    return auth_controller.register_user(email, password, first_name, last_name)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    return auth_controller.login_user(email, password)
