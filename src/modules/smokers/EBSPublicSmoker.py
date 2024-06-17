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
logger = logging.getLogger('cloud-droid')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup timestamp
iso_now_time = datetime.datetime.now().isoformat()

# smoker for ebs snapshot public (creation and delete)


def EBSPublicSmoker():
    ec2 = boto3.resource('ec2')
    snapshot = ec2.Snapshot('')  # put your snapshot ID HERE!
    response = snapshot.describe_attribute(Attribute='createVolumePermission')
    logger.info(" reading ebs properties: "+str(response))
    response = snapshot.modify_attribute(
        Attribute='createVolumePermission',
        CreateVolumePermission={
            'Add': [
                {
                    'Group': 'all'
                },
            ]
        }
    )
    response = snapshot.describe_attribute(Attribute='createVolumePermission')
    logger.info(" changing permissions: "+str(response))
    response = snapshot.modify_attribute(
        Attribute='createVolumePermission',
        CreateVolumePermission={
            'Remove': [
                {
                    'Group': 'all'
                },
            ]
        }
    )
    logger.info(" rolling back permissions: "+str(response))
    response = snapshot.describe_attribute(Attribute='createVolumePermission')
    logger.info("finishing: "+str(response))
    logger.info(' done!')
