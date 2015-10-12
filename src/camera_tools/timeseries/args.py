#!/usr/bin/env python
# -*- coding: utf-8 -*-

from camera_tools.args import parent_parser, create_parser

def parse_args(args):
    parser = create_parser(
        prog='timeseries',
        description='Create a time series from the camera',
        parents=[parent_parser()]
    )
    parser.add_argument(
        'endpoint',
        nargs='?',
        default='http://192.168.122.1:8080',
        help='The endpoint to connect to'
    )
    return parser.parse_args(args)
