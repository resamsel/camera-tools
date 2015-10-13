#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import logging

logger = logging.getLogger(__name__)


class Request(object):
    def __init__(self, method, params=None, id=None, version=None):
        self.method = method

        if params is None:
            params = []
        if id is None:
            id = 1
        if version is None:
            version = "1.0"

        self.params = params
        self.id = id
        self.version = version

    def __str__(self):
        return json.dumps(self.__dict__)


class API(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            return lambda *params: self.invoke(name, params)

    def url(self):
        return '{self.endpoint}/sony/camera'.format(self=self)

    def invoke(self, method, params=None):
        req = Request(method, params)

        logger.debug('API.invoke(url=%s, request=%s)', self.url(), str(req))

        return requests.post(self.url(), str(req)).json()


class APIMock(API):
    def invoke(self, method, params=None):
        req = Request(method, params)

        logger.debug('APIMock.invoke(url=%s, request=%s)', self.url(), str(req))

        return {
            'error': [
                40401,
                'Camera Not Ready ({0}{1})'.format(
                    req.method,
                    req.params
                )
            ],
            'id': req.id
        }
