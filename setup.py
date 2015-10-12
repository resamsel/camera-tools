#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 René Samselnig
#
# This file is part of Database Navigator.
#
# Database Navigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Database Navigator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Database Navigator.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import absolute_import
from setuptools import setup, find_packages


setup(
    name="camera-tools",
    version='0.0.1',
    description="Python camera tools",
    url="https://github.com/resamsel/camera-tools",
    author="René Samselnig",
    author_email="me@resamsel.com",
    license="GPLv3+",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities'
    ],
    keywords="",

    packages=find_packages(
        'src', exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    package_dir={'': 'src'},

    # dependencies
    install_requires=[
        'requests>=2.8.0'
    ],

    entry_points={
        'console_scripts': [
            'timeseries = camera_tools.timeseries:main'
        ]
    }
)
