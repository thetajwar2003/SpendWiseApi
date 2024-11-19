import boto3


def init_dynamodb(config):
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )
    return dynamodb
