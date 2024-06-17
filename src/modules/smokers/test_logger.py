#!/usr/bin/python

import logging

logger = logging.getLogger('siras')
log_format = "%(asctime)s [%(levelname)s]: %(filename)s(%(funcName)s:%(lineno)s) >> %(message)s"
log_date_format = "%m/%d/%Y %I:%M:%S %p"
logFormatter = logging.Formatter(log_format)


def test_message():
    logger.warning(" Executing a 'test' smoker")
    logger.error(" Logging an ERROR level message")
    logger.info(" Logging an INFO level message")
    return 0
