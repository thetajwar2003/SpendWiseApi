class TransactionController:
    def __init__(self, transaction_model):
        self.transaction_model = transaction_model

    def add_transaction(self, transaction):
        self.transaction_model.add_transaction(transaction)
        return {"message": "Transaction added successfully"}, 201

    def get_transactions(self, user_id):
        transactions = self.transaction_model.get_transactions(user_id)
        return {"transactions": transactions}, 200
