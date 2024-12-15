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
            'item_id': None,
            'access_token': None,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        })

    def get_user(self, user_id):
        """
        Retrieve user details by `user_id`.
        """
        response = self.table.get_item(Key={'user_id': user_id})
        return response.get('Item')

    def update_item(self, user_id, **attributes):
        """
        Dynamically update attributes for a user in DynamoDB.

        Args:
            user_id (str): The user ID (Partition Key).
            **attributes: Arbitrary key-value pairs to update or add.
        """
        try:
            # Add the updated_at timestamp dynamically
            attributes['updated_at'] = datetime.utcnow().isoformat()

            # Build the UpdateExpression and ExpressionAttributeValues
            update_expression = "SET " + \
                ", ".join([f"{key} = :{key}" for key in attributes.keys()])
            expression_attribute_values = {
                f":{key}": value for key, value in attributes.items()}

            # Perform the update operation
            self.table.update_item(
                Key={'user_id': user_id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise ValueError("User not found")
            else:
                raise e
