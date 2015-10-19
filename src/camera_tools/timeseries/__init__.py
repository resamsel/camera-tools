#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import urllib

from camera_tools import CameraApp
from camera_tools.sony import API, BusinessException
from camera_tools.op import CameraOp
from camera_tools.op.record import TakePicture

from .args import parser

logger = logging.getLogger(__name__)


def ready(res):
    if res is None or 'error' not in res:
        return True
    return res['error'][0] != 40403


def available(d, key):
    return d is not None and key in d


class APIMock(API):
    def __init__(self, endpoint=None):
        self.camera = self
        self.avContent = self
        self.system = self

        self.id = 1

    def actTakePicture(self, *args):  # noqa
        # pylint: disable=unused-argument
        return ['0']

    def getAvailableApiList(self, *args):  # noqa
        # pylint: disable=unused-argument
        return [['awaitTakePicture', 'actTakePicture']]

    def getVersions(self, *args):  # noqa
        # pylint: disable=unused-argument
        return [['1.0', '1.1', '1.2']]

    def _invoke(self, method, args=None):
        logger.debug('Invoking %s%s', method, args)

        if method == 'getMethodTypes':
            return {'results': [], 'id': self.id}

        return {'result': [''], 'id': self.id}


class TimeSeries(CameraApp):
    def __init__(self, args):
        super(TimeSeries, self).__init__(args)
        if not args.mock:
            self.api = API(args.endpoint)
        else:
            self.api = APIMock(args.endpoint)

        self._take_picture = TakePicture(self.api, **args.__dict__)

    def start(self):
        print 'About to take {args.number_images} picture(s)...'.format(
            args=self.args
        )

        try:
            if self.args.list_f_numbers:
                # pylint: disable=no-member
                op = CameraOp(self.api)
                self.api.camera.startRecMode()
                op.wait_until_idle()
                print self.api.camera.getAvailableFNumber()
                self.api.camera.stopRecMode()
                # pylint: enable=no-member
                return
            self._take_picture()
        except KeyboardInterrupt:
            raise
        except Exception as e:
            logger.warn(
                'Error while recording: %s (%s)\n%s',
                e,
                type(e),
                self.api.camera.getEvent(True))  # pylint: disable=no-member
            raise

        print 'Finished'

    def tear_down_camera(self):
        logger.debug('Tearing down camera')

    def save_latest(self):
        logger.debug('Saving latest picture to %s', self.args.save_dir)

        try:
            # self.wait_until_idle()
            # pylint: disable=no-member
            self.api.camera.setCameraFunction('Contents Transfer')
            # self.wait_until('ContentsTransfer')
            contents = self.api.avContent.getContentList({
                "uri": "storage:memoryCard1",
                "stIdx": 0,
                "cnt": 1,
                "view": "flat",
                "sort": "descending"
            })
            # pylint: enable=no-member
            original = contents[0][0]['content']['original'][0]
            url = original['url']
            filename = original['fileName']
            logger.info('Saving %s as %s', url, filename)
            print '  saving as {1}'.format(filename)
            urllib.urlretrieve(
                url,
                '{0}/{1}'.format(self.args.save_dir, filename)
            )
        except BusinessException as e:
            logger.warn('Could not save latest picture: %s', e)
            print '  could not save (see log file)'
        finally:
            try:
                self.api.camera.setCameraFunction(  # pylint: disable=no-member
                    'Remote Shooting')
            except BusinessException as e:
                logger.warn('Error while resetting camera function: %s', e)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    p = parser()

    try:
        TimeSeries(p.parse_args(argv)).start()
    except KeyboardInterrupt:
        pass
    except StandardError as e:
        raise
    except Exception as e:
        print '{0}: {1}'.format(p.prog, e)
        sys.exit(-1)
