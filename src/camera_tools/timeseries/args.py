#!/usr/bin/env python
# -*- coding: utf-8 -*-

from camera_tools.args import parent_parser, create_parser


def parser():
    parser = create_parser(
        prog='timeseries',
        description='Create a time series from the camera',
        parents=[parent_parser()]
    )
    parser.add_argument(
        'save_dir',
        metavar='save-dir',
        nargs='?',
        default='.',
        help='The directory to save pictures to (default: %(default)s)'
    )
    parser.add_argument(
        '-e', '--endpoint',
        nargs='?',
        default='http://192.168.122.1:8080',
        help='The endpoint to connect to (default: %(default)s)'
    )
    parser.add_argument(
        '-n', '--number-images',
        default=3,
        type=int,
        help='The number of images to take (default: %(default)s)'
    )
    parser.add_argument(
        '-s', '--shutter-speed',
        default='30"',
        help='The duration of the long exposure (default: %(default)s)'
    )
    parser.add_argument(
        '-i', '--iso-speed',
        default='600',
        help='The ISO speed value (default: %(default)s)'
    )
    parser.add_argument(
        '-w', '--white-balance',
        default='Incandescent',
        help='The white balance value (default: %(default)s)'
    )
    parser.add_argument(
        '-f', '--f-number',
        default='3.5',
        help='The F number or aperture value (default: %(default)s)'
    )
    parser.add_argument(
        '-m', '--focus-mode',
        default='AF-S',
        help='The F number or aperture value (default: %(default)s)'
    )
    parser.add_argument(
        '-N', '--no-download',
        dest='download',
        default=True,
        action='store_false',
        help='Do not download pictures from camera (default: %(default)s)'
    )
    parser.add_argument(
        '--list-f-numbers',
        default=False,
        action='store_true',
        help='Show the list of available F numbers'
    )
    parser.add_argument(
        '--mock',
        default=False,
        action='store_true',
        help='Activates mock mode (no camera connection)'
    )

    return parser


def parse_args(args):
    return parser().parse_args(args)
