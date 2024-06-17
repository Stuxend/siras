#!/usr/bin/python

import boto3
import json
import logging
import datetime
import os
import time

# Setup the verbose logger
logger = logging.getLogger('siras')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Standard configurations
region = os.environ['AWS_DEFAULT_REGION']
bucket_name = f"siras-smoke-s3public-nuke-{datetime.datetime.now().date()}"

bucket_policy = {
    'Version': '2012-10-17',
    'Statement': [{
        'Sid': 'PublicReadGetObject',
        'Effect': 'Allow',
        'Principal': '*',
        'Action': ['s3:GetObject'],
        'Resource': f'arn:aws:s3:::{bucket_name}/*'
    }]
}

tags = [
    {"Key": "Department", "Value": "security"},
    {"Key": "Program", "Value": "siras"},
    {"Key": "Purpose", "Value": "siras"}
]

def S3PublicSmoker():
    try:
        # Create S3 client
        s3 = boto3.client('s3', region_name=region)

        # Create bucket
        logger.info(f" creating bucket: {bucket_name}")
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
        add_tags_to_s3_bucket(bucket_name)

        # Set the public access block for the bucket to allow public access
        public_access_block_config = {
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        }
        s3.put_public_access_block(Bucket=bucket_name, PublicAccessBlockConfiguration=public_access_block_config)

        # Set the bucket policy
        bucket_policy_json = json.dumps(bucket_policy)
        s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_json)
        logger.info(" bucket policy set.")

        # Delete objects in the bucket
        s3o = boto3.resource('s3', region_name=region)
        bucket = s3o.Bucket(bucket_name)
        bucket.objects.all().delete()

        # Delete the bucket
        s3.delete_bucket(Bucket=bucket_name)
        logger.info(f" bucket: {bucket_name} deleted.")
        logger.info(" done!")

    except Exception as e:
        logger.error(f" an error occurred: {str(e)}")

def add_tags_to_s3_bucket(bucket_name):
    try:
        # Create S3 client
        s3 = boto3.client('s3', region_name=region)

        # Set the bucket tagging configuration
        tagging_configuration = {
            'TagSet': tags
        }
        # Set the bucket tagging
        s3.put_bucket_tagging(Bucket=bucket_name, Tagging=tagging_configuration)

    except Exception as e:
        logger.error(f" an error occurred: {str(e)}")
