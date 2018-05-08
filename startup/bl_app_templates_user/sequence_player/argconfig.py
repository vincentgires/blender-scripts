import sys
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-aces',
        help='Set a custom ACES colorspace',
        action='store_true',
        default=False,
        required=False)
    parser.add_argument(
        'path',
        help='Path of a directory or a file',
        nargs='?')

    # remove Blender specific arguments from sys.argv
    # to be able to use argparse
    if '--' in sys.argv:
        index = sys.argv.index('--') + 1
        arguments = sys.argv[index:]
        args = parser.parse_args(arguments)
    else:
        args = parser.parse_args()

    return args
