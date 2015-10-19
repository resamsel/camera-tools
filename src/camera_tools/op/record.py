# -*- coding: utf-8 -*-

import logging
import time
import json
import urlparse
import os
import timeout

from camera_tools.op import CameraOp
from camera_tools.sony import BusinessException
from camera_tools.utils import download

logger = logging.getLogger(__name__)

DEFAULTS = {
    'number_images': 1,
    'sleep': 0,
    'exposure_mode': None,
    'shutter_speed': None,
    'white_balance': None,
    'iso_speed': None,
    'f_number': None,
    'focus_mode': 'MF'
}


@timeout.timeout(5)
def download_preview(res, save_dir):
    logger.debug('download_preview(res=%s, save_dir=%s)', res, save_dir)

    try:
        url = res[0][0]
        filename = os.path.basename(urlparse.urlparse(url).path)

        download(url, '{0}/{1}'.format(save_dir, filename))
    except Exception as e:
        logger.warn('Download failed: %s', e.message)


class TakePicture(CameraOp):
    def __init__(self, api, **kwargs):
        super(TakePicture, self).__init__(api)

        self.number_images = 1
        self.sleep = 0
        self.exposure_mode = None
        self.shutter_speed = None
        self.white_balance = None
        self.iso_speed = None
        self.f_number = None
        self.focus_mode = 'MF'
        self.save_dir = '.'

        self.__dict__.update(DEFAULTS)
        self.__dict__.update(kwargs)

    def __call__(self, *args, **kwargs):
        logger.debug(
            'Config: %s',
            json.dumps(
                dict(filter(
                    lambda (k, v): type(v) in (str, unicode, int, float, bool),
                    self.__dict__.iteritems()
                )),
                indent=4,
                separators=(',', ': ')
            )
        )
        self.setup()

        try:
            for i in range(self.number_images):
                self.take_picture()
                if (self.number_images > 1
                        and self.number_images > i+1
                        and self.sleep > 0):
                    # We are in between two shots
                    logger.debug('Sleep for %d', self.sleep)
                    time.sleep(self.sleep)
        finally:
            self.tear_down()

    def setup(self):
        logger.debug('Start rec mode')
        self.start_rec_mode()

        callables = self.available_api_list()
        if self.exposure_mode is not None and 'setExposureMode' in callables:
            self.api.camera.setExposureMode(self.exposure_mode)
        if self.shutter_speed is not None and 'setShutterSpeed' in callables:
            self.api.camera.setShutterSpeed(self.shutter_speed)
        if self.white_balance is not None and 'setWhiteBalance' in callables:
            self.api.camera.setWhiteBalance(self.white_balance, False, -1)
        # self.api.camera.getAvailableFNumber()
        # if self.f_number is not None and 'setFNumber' in callables:
            # self.api.camera.setFNumber(self.f_number)
        if self.iso_speed is not None and 'setIsoSpeedRate' in callables:
            self.api.camera.setIsoSpeedRate(self.iso_speed)
        if self.focus_mode is not None and 'setFocusMode' in callables:
            self.api.camera.setFocusMode(self.focus_mode)

    def tear_down(self):
        logger.debug('Stop rec mode')
        self.stop_rec_mode()

    def take_picture(self):
        logger.debug('Wait for actTakePicture')
        self.wait_until_available('actTakePicture')

        try:
            logger.debug('Take Picture')
            res = self.api.camera.actTakePicture()

            logger.info('Took picture')

            download_preview(res, self.save_dir)
        except BusinessException as e:
            logger.debug(
                'Expecting long exposure error: %s (%d)', e.message, e.code)

            if e.code == 40403:
                # We're expecting a long exposure, so wait until it finishes
                self.wait_until_idle()

                logger.info('Took picture (long exposure)')

                download_preview(
                    self.api.camera.awaitTakePicture(), self.save_dir)
