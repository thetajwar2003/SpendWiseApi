import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    AWS_REGION = os.getenv('AWS_REGION')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
    COGNITO_APP_CLIENT_ID = os.getenv('COGNITO_APP_CLIENT_ID')
    PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
    PLAID_SECRET = os.getenv('PLAID_SECRET')
    PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')  # Default to 'sandbox'
