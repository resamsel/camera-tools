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


class BusinessException(Exception):
    def __init__(self, method, params, code, message):
        super(BusinessException, self).__init__(message)
        self.method = method
        self.params = params
        self.code = code
        self.message = message

    def __str__(self):
        return '{method}{params}: {message} ({code})'.format(**self.__dict__)


class Service(object):
    def __init__(self, endpoint, path, id):
        self.url = '{0}/sony/{1}'.format(endpoint, path)
        self.id = id

        self.versions = {}

        self.init()

    def init(self):
        try:
            method_types = self._invoke(
                'getMethodTypes', ['1.0'])['results']
        except:
            return

        for method_type in method_types:
            self.versions[method_type[0]] = method_type[3]

        logger.debug('Versions: %s', self.versions)

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except:
            return lambda *params: self.invoke(name, params)

    def invoke(self, method, params=None):
        res = self._invoke(method, params)

        if 'error' in res and res['error'][0] != 0:
            raise BusinessException(method, params, *res['error'])

        if 'results' in res:
            return res['results']

        return res['result']

    def _invoke(self, method, params=None):
        logger.debug('Invoking %s%s on %s', method, params, self.url)

        req = Request(
            method,
            params,
            self.id,
            self.versions.get(method, '1.0')
        )

        logger.debug('Request: %s', str(req))

        res = requests.post(self.url, str(req))

        logger.debug('Response: %s', res.content)

        try:
            return res.json()
        except ValueError as e:
            logger.warn('Error while decoding JSON: %s', e.message)
            raise


class Camera(Service):
    def __init__(self, endpoint, id):
        super(Camera, self).__init__(endpoint, 'camera', id)


class AvContent(Service):
    def __init__(self, endpoint, id):
        super(AvContent, self).__init__(endpoint, 'avContent', id)


class System(Service):
    def __init__(self, endpoint, id):
        super(System, self).__init__(endpoint, 'system', id)


class API(object):
    def __init__(self, endpoint='http://192.168.122.1:8080'):
        id = 1
        self.camera = Camera(endpoint, id)
        self.avContent = AvContent(endpoint, id)
        self.system = System(endpoint, id)
