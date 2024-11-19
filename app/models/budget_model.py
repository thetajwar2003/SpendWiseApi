class BudgetModel:
    def __init__(self, dynamodb):
        self.table = dynamodb.Table('SpendWiseBudgets')

    def create_budget(self, user_id, category, amount):
        self.table.put_item(Item={
            'user_id': user_id,
            'category': category,
            'amount': amount
        })

    def get_budgets(self, user_id):
        response = self.table.query(
            KeyConditionExpression="user_id = :user_id",
            ExpressionAttributeValues={":user_id": user_id}
        )
        return response.get('Items', [])

    def update_budget(self, user_id, category, new_amount):
        self.table.update_item(
            Key={'user_id': user_id, 'category': category},
            UpdateExpression="SET amount = :amount",
            ExpressionAttributeValues={":amount": new_amount}
        )

    def delete_budget(self, user_id, category):
        self.table.delete_item(Key={'user_id': user_id, 'category': category})
