from flask import Blueprint, request, jsonify, current_app
from ..controllers.plaid_controller import PlaidController

plaid_bp = Blueprint('plaid_bp', __name__)
plaid_controller = PlaidController(current_app.plaid_client)


@plaid_bp.route('/create_link_token', methods=['POST'])
def create_link_token():
    data = request.json
    user_id = data.get('user_id')
    link_token = plaid_controller.create_link_token(user_id)
    return jsonify({'link_token': link_token})


@plaid_bp.route('/exchange_public_token', methods=['POST'])
def exchange_public_token():
    data = request.json
    public_token = data.get('public_token')
    access_token, item_id = plaid_controller.exchange_public_token(
        public_token)
    # Save access_token and item_id securely
    return jsonify({'access_token': access_token, 'item_id': item_id})
