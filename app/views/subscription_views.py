from flask import Blueprint, request, jsonify, current_app
from ..models.subscription_model import SubscriptionModel
from ..controllers.subscription_controller import SubscriptionController

subscription_bp = Blueprint('subscription_bp', __name__)
subscription_model = SubscriptionModel(current_app.dynamodb)
subscription_controller = SubscriptionController(subscription_model)


@subscription_bp.route('/', methods=['POST'])
def add_subscription():
    data = request.json
    return subscription_controller.add_subscription(data)


@subscription_bp.route('/', methods=['GET'])
def get_subscriptions():
    user_id = request.args.get('user_id')
    return subscription_controller.get_subscriptions(user_id)


@subscription_bp.route('/<string:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    return subscription_controller.delete_subscription(subscription_id)
