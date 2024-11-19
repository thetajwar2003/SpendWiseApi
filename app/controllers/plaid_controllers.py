class PlaidController:
    def __init__(self, plaid_client):
        self.plaid_client = plaid_client

    def create_link_token(self, user_id):
        response = self.plaid_client.LinkToken.create({
            'user': {'client_user_id': user_id},
            'client_name': 'SpendWise',
            'products': ['transactions'],
            'country_codes': ['US'],
            'language': 'en',
            'redirect_uri': 'https://your-redirect-uri.com',
        })
        return response['link_token']

    def exchange_public_token(self, public_token):
        response = self.plaid_client.Item.public_token.exchange(public_token)
        return response['access_token'], response['item_id']
