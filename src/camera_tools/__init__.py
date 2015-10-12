#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


class CameraOp(object):
    def __init__(self, args):
        self.args = args

        logging.basicConfig(
            stream=args.logfile,
            level=args.loglevel,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")
