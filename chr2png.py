#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2018 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from __future__ import division, absolute_import, print_function, unicode_literals
import six

import locale
import argparse

# Use https://gitgud.io/snippets/182 algorithm, but made more simple and verbose, and flexible

def bytetobits(byte):
    # All bits from large to small (left-to-right)
    for bit in list(reversed(range(8))):
        yield bool(byte & (2 ** bit))

def main():
    parser = argparse.ArgumentParser(description='Convert from CHR to PNG')
    parser.add_argument('-V', '--version', action='version', version='0.0.0')

    args = parser.parse_args()

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    main()

