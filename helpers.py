# # in util/helpers.py

import boto3, botocore

config = Config(
    region_name = 'eu-central-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

s3_client = boto3.client('s3', config=config)