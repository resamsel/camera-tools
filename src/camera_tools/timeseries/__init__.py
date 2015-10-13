#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from camera_tools import CameraOp
from camera_tools.sony import API, APIMock

from .args import parse_args


def ready(res):
    if res is None or res['error'] is None:
        return True
    return res['error'][0] != 40403


class TimeSeries(CameraOp):
    def __init__(self, args):
        super(TimeSeries, self).__init__(args)
        if not args.mock:
            self.api = API(args.endpoint)
        else:
            self.api = APIMock(args.endpoint)

    def start(self):
        try:
            yield self.api.startRecMode()

            for i in self.backup_camera():
                yield i

            for i in self.prepare_camera():
                yield i

            for i in xrange(self.args.number_images):
                yield self.take_picture()
        finally:
            for i in self.restore_camera():
                yield i
            yield self.api.stopRecMode()

    def backup_camera(self):
        """Backs up the camera config"""

        self.exposure_mode = self.api.getExposureMode()
        self.shutter_speed = self.api.getShutterSpeed()
        self.white_balance = self.api.getWhiteBalance()

        yield self.exposure_mode
        yield self.shutter_speed
        yield self.white_balance

    def restore_camera(self):
        """Restores the camera config to its original values"""

        if 'result' in self.exposure_mode:
            yield self.api.setExposureMode(self.exposure_mode['result'][0])
        else:
            yield
        if 'result' in self.shutter_speed:
            yield self.api.setShutterSpeed(self.shutter_speed['result'][0])
        else:
            yield
        if 'result' in self.white_balance:
            yield self.api.setWhiteBalance(self.white_balance['result'][0])
        else:
            yield

    def prepare_camera(self):
        yield self.api.setExposureMode('Manual')
        yield self.api.setShutterSpeed('30"')
        yield self.api.setWhiteBalance('Incandescent')

    def take_picture(self):
        while not ready(self.api.awaitTakePicture()):
            time.sleep(1)
        return self.api.actTakePicture()
        

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    try:
        for i in TimeSeries(parse_args(args)).start():
            print i
    except KeyboardInterrupt:
        pass
