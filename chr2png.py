#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2018 Taylor C. Richberger <taywee@gmx.com>
# This code is released under the license described in the LICENSE file

from __future__ import division, absolute_import, print_function, unicode_literals

from itertools import count, chain
import sys
import locale
import argparse

import png

def bytetobits(byte):
    '''Takes a byte (as an int) and returns an iterator to iterate per-bit'''
    # All bits from large to small (left-to-right)
    for bit in list(reversed(range(8))):
        yield bool(byte & (1 << bit))

def processtile(rawtile):
    '''Take in a raw 16-byte array for a tile and process it into its final
    form.  Yield index numbers.  This is a generator that yields generators of
    rows.'''

    rawtile = list(rawtile)

    # generator for a plane.  Each plane is a generator of generators, where
    # each inner generator yields a row bit-by-bit
    first = (bytetobits(byte) for byte in rawtile[:8])
    second = (bytetobits(byte) for byte in rawtile[8:])

    # yield row generators.  First is bit 0
    for row0, row1 in zip(first, second):
        yield (int(bit0) | (int(bit1) << 1) for bit0, bit1 in zip(row0, row1))


def main():
    parser = argparse.ArgumentParser(description='Convert from CHR to PNG')
    parser.add_argument('-V', '--version', action='version', version='0.1.0')
    parser.add_argument('-i', '--input', help='Input CHR file (default stdin)',
        type=argparse.FileType('rb'), default=sys.stdin.buffer)
    parser.add_argument('-o', '--output', help='Output PNG file (default stdout)',
        type=argparse.FileType('wb'), default=sys.stdout.buffer)
    args = parser.parse_args()

    tiles = []
    for tilenum in count():
        rawtile = args.input.read(16)
        if len(rawtile) == 0:
            break
        if len(rawtile) != 16:
            raise RuntimeError('Input file not a multiple of 16 bytes')
        tiles.append(processtile(rawtile))


    palette = (
        # Black
        (0x00, 0x00, 0x00, 0xff),
        # Red
        (0xff, 0x00, 0x00, 0xff),
        # Green
        (0x00, 0xff, 0x00, 0xff),
        # Blue
        (0x00, 0x00, 0xff, 0xff),
    )

    rowlist = []
    for y in range(32):
        starttile = y * 16
        tilerow = tiles[starttile:starttile + 16]

        # This is a little mystical.  Basically, it uses zip to interleave
        # individual rows in each tile in the row, and then chain to combine
        # them, so that you get full-length PNG rows
        rowlist.extend(chain(*rows) for rows in zip(*tilerow))
    writer = png.Writer(128, 256, palette=palette, bitdepth=2)
    writer.write(args.output, rowlist)

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    main()
