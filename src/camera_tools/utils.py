# -*- coding: utf-8 -*-

import urllib
import logging

logger = logging.getLogger(__name__)


def download(url, target):
    logger.debug('Downloading %s into %s...', url, target)

    urllib.urlretrieve(url, target)

    logger.debug('Downloaded into %s', target)
