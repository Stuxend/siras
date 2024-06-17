#!/usr/bin/python

import boto3
import json
import logging
import datetime
import os
import gzip
import sys
from io import BytesIO
from botocore.exceptions import ClientError
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# from .loggerELK import sendToELK

##### define standard configurations ####

# Setup the verbose logger
logger = logging.getLogger('siras')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup timestamp
iso_now_time = datetime.datetime.now().isoformat()

# smoker for loca aws admin creation


def AWSadminSmoker():
    TAG = [
        {"Key": "Department", "Value": "security"},
        {"Key": "Program", "Value": "siras"},
        {"Key": "Purpose", "Value": "siras"}
    ]
    descript = ' siras smoke iam localuser ' + iso_now_time
    name = ' siras_smoke_user'
    iam = boto3.client('iam')
    logger.info(' creating the user siras-ADMIN')
    response = iam.create_user(UserName='siras-ADMIN', Tags=TAG)
    user_id = response['User']['UserId']
    user_arn = response['User']['Arn']
    logger.info(
        ' Attaching the user to "AdministratorAccess" policy')
    iam.attach_user_policy(
        UserName='siras-ADMIN',
        PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess'
    )
    logger.info(' user Created: ' +
                " ID: " + user_id + " ARN: " + user_arn)
    logger.info(' rollback of the user now')
    iam.detach_user_policy(
        UserName='siras-ADMIN',
        PolicyArn='arn:aws:iam::aws:policy/AdministratorAccess'
    )
    iam.delete_user(UserName='siras-ADMIN')
    logger.info(' done!')
