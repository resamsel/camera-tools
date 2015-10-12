#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from camera_tools import CameraOp
from camera_tools.sony import API

from .args import parse_args


class TimeSeries(CameraOp):
    def __init__(self, args):
        super(TimeSeries, self).__init__(args)
        self.api = API(args.endpoint)

    def start(self):
        yield 'startRecMode', self.api.startRecMode()
        yield 'stopRecMode', self.api.stopRecMode()


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    for i in TimeSeries(parse_args(args)).start():
        print i
