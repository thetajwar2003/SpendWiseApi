class TransactionModel:
    def __init__(self, dynamodb):
        self.table = dynamodb.Table('SpendWiseTransactions')

    def add_transaction(self, transaction):
        self.table.put_item(Item=transaction)

    def get_transactions(self, user_id):
        response = self.table.query(
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        return response.get('Items', [])
