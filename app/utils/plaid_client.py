from plaid import Client


def init_plaid_client(config):
    client = Client(
        client_id=config.PLAID_CLIENT_ID,
        secret=config.PLAID_SECRET,
        environment=config.PLAID_ENV
    )
    return client
