# -*- coding: utf-8 -*-

import sys

from camera_tools import CameraApp
from camera_tools.op.record import TakePicture
from camera_tools.args import create_parser, parent_parser
from camera_tools import timeseries


def pprint(d):
    import json
    print json.dumps(
        d,
        indent=4,
        separators=(',', ': ')
    )


class Remote(CameraApp):
    def __init__(self, args):
        super(Remote, self).__init__(args)
        # api = sony.API()
        api = timeseries.APIMock()
        self.camera = api.camera
        self.avContent = api.avContent
        self.system = api.system


def main():
    args = create_parser(
        prog='sony-remote',
        description='Test tool for the sony remote camera api',
        parents=[parent_parser()]
    ).parse_args(sys.argv[1:])

    op = Remote(args)

    # pprint(op.camera.startRecMode())
    # pprint(op.camera.getSupportedShootMode())
    # pprint(op.camera.stopRecMode())

    tp = TakePicture(
        op, count=5, sleep=0, exposure_mode='Shutter', shutter_speed='2"')
    tp()
