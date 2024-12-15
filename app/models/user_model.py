from datetime import datetime


class UserModel:
    def __init__(self, dynamodb):
        self.table = dynamodb.Table('spend-wise-users')

    def create_user(self, user_id, email, first_name, last_name):
        """
        Create a new user entry in DynamoDB.
        """
        self.table.put_item(Item={
            'user_id': user_id,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'created_at': datetime.utcnow().isoformat()
        })

    def get_user(self, user_id):
        """
        Retrieve user details by `user_id`.
        """
        response = self.table.get_item(Key={'user_id': user_id})
        return response.get('Item')

    def update_user(self, user_id, updates):
        """
        Update user data in DynamoDB.
        """
        expression = ", ".join(f"{key}=:{key}" for key in updates.keys())
        attribute_values = {f":{key}": value for key, value in updates.items()}

        self.table.update_item(
            Key={'user_id': user_id},
            UpdateExpression=f"SET {expression}",
            ExpressionAttributeValues=attribute_values
        )
