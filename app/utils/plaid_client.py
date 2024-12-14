from plaid.api import plaid_api
from plaid.configuration import Configuration
from plaid.api_client import ApiClient


def init_plaid_client(config):
    # Create Plaid API client using updated API
    configuration = Configuration(
        host=f"https://{config['PLAID_ENV']}.plaid.com",
        api_key={
            'clientId': config['PLAID_CLIENT_ID'],
            'secret': config['PLAID_SECRET'],
        },
    )
    api_client = ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)
