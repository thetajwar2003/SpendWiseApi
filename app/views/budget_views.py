from flask import Blueprint, request, jsonify, current_app
from ..models.budget_model import BudgetModel
from ..controllers.budget_controller import BudgetController

budget_bp = Blueprint('budget_bp', __name__)
budget_model = BudgetModel(current_app.dynamodb)
budget_controller = BudgetController(budget_model)


@budget_bp.route('/', methods=['POST'])
def create_budget():
    data = request.json
    user_id = data.get('user_id')
    category = data.get('category')
    amount = data.get('amount')
    return budget_controller.create_budget(user_id, category, amount)


@budget_bp.route('/', methods=['GET'])
def get_budgets():
    user_id = request.args.get('user_id')
    return budget_controller.get_budgets(user_id)


@budget_bp.route('/<string:category>', methods=['PUT'])
def update_budget(category):
    data = request.json
    user_id = data.get('user_id')
    new_amount = data.get('amount')
    return budget_controller.update_budget(user_id, category, new_amount)


@budget_bp.route('/<string:category>', methods=['DELETE'])
def delete_budget(category):
    user_id = request.args.get('user_id')
    return budget_controller.delete_budget(user_id, category)
