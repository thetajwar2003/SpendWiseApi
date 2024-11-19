from flask import Blueprint, request, jsonify, current_app
from ..models.transaction_model import TransactionModel
from ..controllers.transaction_controller import TransactionController

transaction_bp = Blueprint('transaction_bp', __name__)
transaction_model = TransactionModel(current_app.dynamodb)
transaction_controller = TransactionController(transaction_model)


@transaction_bp.route('/', methods=['POST'])
def add_transaction():
    data = request.json
    return transaction_controller.add_transaction(data)


@transaction_bp.route('/', methods=['GET'])
def get_transactions():
    user_id = request.args.get('user_id')
    return transaction_controller.get_transactions(user_id)
