from flask import Blueprint, request, jsonify, current_app
from ..controllers.plaid_controller import PlaidController

# Define Blueprint correctly
plaid_bp = Blueprint('plaid_bp', __name__)


@plaid_bp.route('/create_link_token', methods=['POST'])
def create_link_token():
    # Access the Plaid client from the current app context
    plaid_client = current_app.plaid_client
    plaid_controller = PlaidController(plaid_client)

    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        link_token = plaid_controller.create_link_token(user_id)
        return jsonify({'link_token': link_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@plaid_bp.route('/exchange_public_token', methods=['POST'])
def exchange_public_token():
    # Access the Plaid client from the current app context
    plaid_client = current_app.plaid_client
    plaid_controller = PlaidController(plaid_client)

    data = request.json
    public_token = data.get('public_token')
    if not public_token:
        return jsonify({'error': 'Public token is required'}), 400

    try:
        access_token, item_id = plaid_controller.exchange_public_token(
            public_token)
        return jsonify({'access_token': access_token, 'item_id': item_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
