# in util/helpers.py

import boto3, botocore

s3 = boto3.client(
    "s3"
)