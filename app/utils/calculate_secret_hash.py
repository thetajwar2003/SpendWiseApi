import base64
import hmac
import hashlib


def calculate_secret_hash(client_id, client_secret, username):
    """
    Calculate the Cognito SECRET_HASH parameter for secure communication.
    """
    message = username + client_id
    digest = hmac.new(
        client_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(digest).decode('utf-8')
