#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2018 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from __future__ import division, absolute_import, print_function, unicode_literals

import sys
import locale
import argparse

import png

def take(it, size):
    '''Yield n values from iterator'''
    for i in range(size):
        yield next(it)

def chunks(iterable, size):
    '''Yield size-sized chunks from iterable'''
    it = iter(iterable)
    while True:
        chunk = tuple(item for item in take(it, size))
        if not chunk:
            return
        yield chunk

# iterate through an image and yield tiles one at a time as they are extracted
def gettiles(image):
    rowchunks = []
    for row in image:
        # rowchunks should be a list of rows, with each row being chunks of 8
        # bytes
        rowchunks.append(chunk for chunk in chunks(row, 8))
        if len(rowchunks) == 8:
            for tile in zip(*rowchunks):
                yield (byte for row in tile for byte in row)
            rowchunks = []
    assert not rowchunks, 'gettiles should not have leftover data'

def rowtobytes(row):
    '''Take a row of 8 integers and return a tuple of two bytes from it'''
    it = iter(row)
    byte1 = 0
    byte2 = 0
    for bit in list(reversed(range(8))):
        byte = next(it)
        byte1 |= (1 & byte) << bit
        byte2 |= (1 & (byte >> 1)) << bit
    return byte1, byte2


def processtile(rawtile):
    '''Take in an iterable of 64 bytes; yield 16 bytes in compressed CHR
    form.'''

    first = []
    second = []

    # Rowtobytes gives data in iterations of planebyte1, planebyte2, etc
    planes = zip(*(rowtobytes(row) for row in chunks(rawtile, 8)))
    for plane in planes:
        for byte in plane:
            yield byte

def main():
    parser = argparse.ArgumentParser(description='Convert from PNG to CHR')
    parser.add_argument('-V', '--version', action='version', version='0.1.0')
    parser.add_argument('-i', '--input', help='Input PNG file (default stdin)',
        type=argparse.FileType('rb'), default=sys.stdin.buffer)
    parser.add_argument('-o', '--output', help='Output CHR file (default stdout)',
        type=argparse.FileType('wb'), default=sys.stdout.buffer)
    args = parser.parse_args()

    reader = png.Reader(file=args.input)
    width, height, image, meta = reader.read()

    if width % 8 != 0:
        raise RuntimeError('Input file not correct width')
    if height % 8 != 0:
        raise RuntimeError('Input file not correct height')
    if meta['bitdepth'] != 2:
        raise RuntimeError('Input file not correct bit depth (must be 2)')

    for tile in gettiles(image):
        for byte in processtile(tile):
            args.output.write(bytes((byte,)))

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    main()
