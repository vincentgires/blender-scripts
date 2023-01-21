import sys


def get_args(parser):
    # remove Blender specific arguments from sys.argv
    # to be able to use argparse
    if '--' in sys.argv:
        index = sys.argv.index('--') + 1
        arguments = sys.argv[index:]
        args = parser.parse_args(arguments)
    else:
        args = parser.parse_args()

    return args
