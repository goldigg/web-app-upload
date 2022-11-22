import argparse
import logging
from botocore.exceptions import ClientError
import requests



logger = logging.getLogger(__name__)

def generate_presigned_url(s3_client,  method_parameters, expires_in):
    try:
        url = s3_client.generate_presigned_post(
            Bucket=method_parameters['Bucket'],
            Key=method_parameters['Key'],
            ExpiresIn=expires_in
        )
        logger.info("Got presigned URL: %s", url)
    except ClientError:
        logger.exception(
            "Couldn't get a presigned URL for")
        raise
    return url

