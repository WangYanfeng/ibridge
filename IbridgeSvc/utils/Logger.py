#!/bin/python

import logging
import logging.config

logging.config.fileConfig("/usr/ibridge/IbridgeSvc/conf/logger.conf")

console_logger = logging.getLogger('root')
ibLogger = logging.getLogger('ibridge')

