# -*- coding: utf-8 -*-

import time


class CameraOp(object):
    def __init__(self, api):
        self.api = api

    def __call__(self, *args, **kwargs):
        """To be implemented by the subclass"""

        raise Exception('To be implemented by the subclass')

    def camera_status(self):
        status = self.api.camera.getEvent(False)[1]

        if type(status) is dict:
            return status.get('cameraStatus')

        return None

    def wait_until(self, *statii):
        while self.camera_status() not in statii:
            time.sleep(1)

    def wait_until_idle(self):
        self.wait_until('IDLE')

    def wait_until_available(self, method):
        while method not in self.available_api_list():
            time.sleep(1)

    def available_api_list(self):
        return self.api.camera.getAvailableApiList()[0]

    def start_rec_mode(self):
        if 'startRecMode' in self.available_api_list():
            self.api.camera.startRecMode()

    def stop_rec_mode(self):
        if 'stopRecMode' in self.available_api_list():
            self.api.camera.stopRecMode()
