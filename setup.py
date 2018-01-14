#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2017 Absolute Performance Inc <csteam@absolute-performance.com>.
# All rights reserved.
# This is proprietary software.
# No warranty, explicit or implicit, provided.

from setuptools import setup

setup(
    name='png2chr',
    version='0.0.0',
    description='Simple two-file library to convert between a 4-index PNG file and NES CHR file',
    author='Taylor C. Richberger <taywee@gmx.com>',
    author_email='taywee@gmx.com',
    url='https://github.com/Taywee/png2chr',
    license='GPL3',
    entry_points={
        'console_scripts': [
            'png2chr = png2chr:main',
            'chr2png = chr2png:main',
            ]
        },
    py_modules=[
        'png2chr',
        'chr2png',
        ],
    install_requires=[
        'six',
        'pypng',
        ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Embedded Systems',
        ],
)
