class SubscriptionController:
    def __init__(self, subscription_model):
        self.subscription_model = subscription_model

    def add_subscription(self, subscription):
        self.subscription_model.add_subscription(subscription)
        return {"message": "Subscription added successfully"}, 201

    def get_subscriptions(self, user_id):
        subscriptions = self.subscription_model.get_subscriptions(user_id)
        return {"subscriptions": subscriptions}, 200

    def delete_subscription(self, subscription_id):
        self.subscription_model.delete_subscription(subscription_id)
        return {"message": "Subscription deleted successfully"}, 200
