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

##### define standard configurations ####

# Setup the verbose logger
logger = logging.getLogger('cloud-droid')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup timestamp
iso_now_time = datetime.datetime.now().isoformat()


# AWS ACCOUNT ID.
account_id = ''

# smoker for aws console auth faild


def awsConsoleAuthSmoker():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    logger.info(' testing auth fail to aws console root')
    headers = {
        'Origin': 'https://signin.aws.amazon.com',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'droid (Security Incident Response Automated Simulations)',
        'Referer': 'https://signin.aws.amazon.com/oauth?redirect_uri=https%3A%2F%2Fconsole.aws.amazon.com%2Fconsole%2Fhome%3Fstate%3DhashArgs%2523%26isauthcode%3Dtrue&client_id=arn%3Aaws%3Aiam%3A%3A'+account_id+'%3Auser%2Fhomepage&response_type=code&iam_user=true&account='+account_id,
    }
    data = {
        'action': 'iam-user-authentication',
        'account': account_id,
        'username': 'droid-testing',
        'password': 'fake123123fake',
        'client_id': 'arn%3Aaws%3Aiam%3A%3A015428540659%3Auser%2Fhomepage',
        'redirect_uri': 'https%3A%2F%2Fconsole.aws.amazon.com%2Fconsole%2Fhome%3Fstate%3DhashArgs%2523%26isauthcode%3Dtrue'
    }
    logger.info(' testing user: droid-testing into '+account_id+' account')
    time.sleep(5)
    response = requests.post(
        'https://signin.aws.amazon.com/authenticate', headers=headers, data=data, verify=False)
    logger.info(' this takes a while ...')
    time.sleep(5)
    response = requests.post(
        'https://signin.aws.amazon.com/authenticate', headers=headers, data=data, verify=False)
    time.sleep(5)
    response = requests.post(
        'https://signin.aws.amazon.com/authenticate', headers=headers, data=data, verify=False)
    logger.info(' still working....')
    time.sleep(5)
    response = requests.post(
        'https://signin.aws.amazon.com/authenticate', headers=headers, data=data, verify=False)
    time.sleep(5)
    response = requests.post(
        'https://signin.aws.amazon.com/authenticate', headers=headers, data=data, verify=False)
    logger.info(' done!')
