#!/usr/bin/python

import boto3
import json
import logging
import datetime
from botocore.exceptions import ClientError
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

##### define standard configurations ####

# Setup the verbose logger
logger = logging.getLogger('siras')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup timestamp
iso_now_time = datetime.datetime.now().isoformat()

# smoker for cloudtrail (creation and delete)
region = os.environ['AWS_DEFAULT_REGION']

def CTrailSmoker():
    try:
        name = "siras_smoke_cloudtrail"
        bucket_name = "siras-smoke-cloudtrail"
        TAG = [
            {"Key": "Department", "Value": "security"},
            {"Key": "Program", "Value": "siras"},
            {"Key": "Purpose", "Value": "siras"}
        ]
        # policy for bucket
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "AWSCloudTrailAclCheck20150319",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "cloudtrail.amazonaws.com"
                    },
                    "Action": "s3:GetBucketAcl",
                    "Resource": "arn:aws:s3:::siras-smoke-cloudtrail"
                },
                {
                    "Sid": "AWSCloudTrailWrite20150319",
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "cloudtrail.amazonaws.com"
                    },
                    "Action": "s3:PutObject",
                    "Resource": "arn:aws:s3:::siras-smoke-cloudtrail/*",
                    "Condition": {
                        "StringEquals": {
                            "s3:x-amz-acl": "bucket-owner-full-control"
                        }
                    }
                }
            ]
        }
        # Create s3 bucket
        s3 = boto3.client('s3', region_name=region)
        logger.info(" creating bucket named: "+bucket_name)
        bucket = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
        # set bucketpolicy
        bucket_policy = json.dumps(policy)
        s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
        # Create cloudtrail
        logger.info(" creating cloudtrail named: "+name)
        client = boto3.client('cloudtrail', region_name=region)
        response = client.create_trail(Name=name, S3BucketName=bucket_name)
        logger.info(" detailed info: "+str(response))
        logger.info(" starting the trail")
        response = client.start_logging(Name=name)
        logger.info(" detailed info: "+str(response))
        logger.info(' deleting trail now')
        response = client.delete_trail(Name=name)
        logger.info(" detailed info: "+str(response))
        logger.info(' deleting s3 now')
        # delete objects
        s3o = boto3.resource('s3', region_name=region)
        bucket = s3o.Bucket(bucket_name)
        bucket.objects.all().delete()
        # delete bucket now
        delete_bucket = s3.delete_bucket(Bucket=bucket_name)
        logger.info(" detailed info: "+str(delete_bucket))
        logger.info(' done!')
    except ClientError as e:
        logger.error(f" an error occurred: {e.response['Error']['Message']}")
        # Handle the error or raise it again if needed