#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2018 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from __future__ import division, absolute_import, print_function, unicode_literals
import six

import locale
import argparse

VERSION = '0.0.0'

def main():
    parser = argparse.ArgumentParser(description='Convert from PNG to CHR')
    parser.add_argument('-V', '--version', action='version', version=VERSION)
    args = parser.parse_args()

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    main()

