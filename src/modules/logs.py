#!/usr/bin/python

import logging
import logging.handlers
import boto3
import json
import logging
import datetime
import os
import sys
import requests
import time
import io
import atexit
import gzip

iso_now_time = datetime.datetime.now().isoformat()


def droid_logger(name):
    # logger settings
    logger = logging.getLogger(name)
    log_format = "%(asctime)s [%(levelname)s]: %(filename)s(%(funcName)s:%(lineno)s) >> %(message)s"

    # print log messages to console
    consoleHandler = logging.StreamHandler()
    logger.propagate = False
    logFormatter = logging.Formatter(log_format)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    return logger


def droid_s3_logger(name):
    # logger settings
    log_stringio = io.StringIO()
    log_format = "%(asctime)s [%(levelname)s]: %(filename)s(%(funcName)s:%(lineno)s) >> %(message)s"
    logger = logging.getLogger(name)
    consoleHandler = logging.StreamHandler()
    logger.propagate = False
    logFormatter = logging.Formatter(log_format)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)
    handler = logging.StreamHandler(log_stringio)
    handler.setFormatter(logFormatter)
    logger.addHandler(handler)
    atexit.register(s3Log, body=log_stringio)
    return logger


def s3Log(body):
    # This take the data form the handler and put a bulk of events into a
    # s3 bucket with gzip file.
    buf = io.BytesIO()
    s3 = boto3.resource('s3', region_name=os.environ['AWS_REGION'])
    year = datetime.datetime.now().strftime("%Y")
    month = datetime.datetime.now().strftime("%m")
    filename = "droid-LOG" + 'T' + iso_now_time + ".log.gz"
    bucketID = os.environ['BUCKETS3']
    key = 'logs/droid/' + year + '/' + month + '/' + filename

    with gzip.GzipFile(fileobj=buf, mode='wb') as gfh:
        with io.TextIOWrapper(gfh, encoding='utf-8') as wrapper:
            wrapper.write(body.getvalue())
    buf.seek(0)
    s3.Bucket(bucketID).put_object(Key=key, Body=buf)
