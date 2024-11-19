class SubscriptionModel:
    def __init__(self, dynamodb):
        self.table = dynamodb.Table('SpendWiseSubscriptions')

    def add_subscription(self, subscription):
        self.table.put_item(Item=subscription)

    def get_subscriptions(self, user_id):
        response = self.table.query(
            KeyConditionExpression="user_id = :user_id",
            ExpressionAttributeValues={":user_id": user_id}
        )
        return response.get('Items', [])

    def delete_subscription(self, subscription_id):
        self.table.delete_item(Key={'subscription_id': subscription_id})
