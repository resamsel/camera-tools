# -*- coding: utf-8 -*-

import argparse
import logging
import os

PARSER_ARGS = {
    # 'formatter_class': argparse.RawDescriptionHelpFormatter,
    'epilog': """Contact:
  If you experience bugs or want to request new features please visit
  <https://github.com/resamsel/python-sony/issues>"""
}


def default_log_file(dirs=None):
    if dirs is None:
        dirs = ['/var/log', '/usr/local/var/log', '/tmp']
    for d in dirs:
        if os.access(d, os.W_OK):
            return os.path.join(d, 'camera-tools.log')
    return os.path.expanduser('~/camera-tools.log')


def parent_parser():
    parser = argparse.ArgumentParser(add_help=False)
    group = parser.add_argument_group('logging')
    group.add_argument(
        '--debug',
        dest='loglevel',
        action='store_const',
        const=logging.DEBUG,
        default=logging.INFO,
        help='set loglevel to debug')
    group.add_argument(
        '--info',
        dest='loglevel',
        action='store_const',
        const=logging.INFO,
        help='set loglevel to info')
    group.add_argument(
        '--warning',
        dest='loglevel',
        action='store_const',
        const=logging.WARNING,
        help='set loglevel to warning')
    group.add_argument(
        '--error',
        dest='loglevel',
        action='store_const',
        const=logging.ERROR,
        help='set loglevel to error')
    group.add_argument(
        '--critical',
        dest='loglevel',
        action='store_const',
        const=logging.CRITICAL,
        help='set loglevel to critical')
    group.add_argument(
        '-L',
        '--logfile',
        type=argparse.FileType('a'),
        default=default_log_file(),
        help='the file to log to')

    return parser


def create_parser(**kwargs):
    kwargs.update(PARSER_ARGS)
    return argparse.ArgumentParser(**kwargs)
