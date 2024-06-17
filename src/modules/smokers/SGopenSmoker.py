#!/usr/bin/python

import boto3
import logging
import datetime
from botocore.exceptions import ClientError


##### define standard configurations ####

# Setup the verbose logger
logger = logging.getLogger('cloud-droid')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup timestamp
iso_now_time = datetime.datetime.now().isoformat()

# smoker for security open group


def SGopenSmoker():
    tags = [
        {"Key": "Department", "Value": "security"},
        {"Key": "Program", "Value": "droid"},
        {"Key": "Purpose", "Value": "droid"}
    ]
    description = 'droid smoke security group ' + iso_now_time
    group_name = 'droid_smoke_group'
    
    ec2 = boto3.client('ec2')
    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    try:
        response = ec2.create_security_group(
            GroupName=group_name,
            Description=description,
            VpcId=vpc_id
        )
        security_group_id = response['GroupId']
        logger.info(' security Group Created %s in vpc %s.' %
                    (security_group_id, vpc_id))

        data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )
        logger.info(' ingress Successfully Set: %s' % data)
    except ClientError as e:
        logger.info(e)

    try:
        response = ec2.delete_security_group(GroupId=security_group_id)
        logger.info(' security Group Deleted')
    except ClientError as e:
        logger.info(e)
