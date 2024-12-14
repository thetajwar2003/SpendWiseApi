from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode


class PlaidController:
    def __init__(self, plaid_client):
        self.plaid_client = plaid_client

    def create_link_token(self, user_id):
        request = LinkTokenCreateRequest(
            user={
                "client_user_id": user_id,
            },
            client_name="SpendWise",
            products=[Products("transactions")],
            country_codes=[CountryCode('US')],  # Fixed: Using CountryCode enum
            language="en",
            redirect_uri="http://localhost:3000/dashboard",
        )
        response = self.plaid_client.link_token_create(request)
        return response.to_dict()["link_token"]

    def exchange_public_token(self, public_token):
        # Updated Public Token Exchange logic
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = self.plaid_client.item_public_token_exchange(request)
        access_token = response.to_dict()["access_token"]
        item_id = response.to_dict()["item_id"]
        return access_token, item_id
