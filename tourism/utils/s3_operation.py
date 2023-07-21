import boto3
import sys
from tourism.exception import CustomException
from tourism.logger import logging

def download_from_s3(bucket_name, object_name, filename):
    try:
        logging.info("Downloading from S3 bucket: %s" % bucket_name)
        s3 = boto3.client('s3')
        s3.download_file(bucket_name, object_name, filename)
        logging.info("Downloaded from S3 bucket: %s" % bucket_name)
    except Exception as e:
        raise CustomException(e, sys) from e