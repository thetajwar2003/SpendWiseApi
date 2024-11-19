class UserModel:
    def __init__(self, dynamodb):
        self.table = dynamodb.Table('SpendWiseUsers')

    def create_user(self, user_id, email, first_name, last_name):
        self.table.put_item(Item={
            'user_id': user_id,
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        })

    def get_user(self, user_id):
        response = self.table.get_item(Key={'user_id': user_id})
        return response.get('Item')
