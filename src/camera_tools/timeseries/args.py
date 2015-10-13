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
    parser.add_argument(
        '-n', '--number-images',
        default=3,
        type=int,
        help='The number of images to take'
    )
    parser.add_argument(
        '--mock',
        default=False,
        action='store_true',
        help='Activates mock mode (no camera connection)'
    )
    return parser.parse_args(args)
