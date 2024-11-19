import boto3


def init_cognito(config):
    cognito = boto3.client(
        'cognito-idp',
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )
    return cognito
