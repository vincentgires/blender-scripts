import sys
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-input',
        help='File input',
        required=False)
    parser.add_argument(
        '-leftinput',
        help='File input for stereoscopic render',
        required=False)
    parser.add_argument(
        '-rightinput',
        help='File input for stereoscopic render',
        required=False)
    parser.add_argument(
        '-startframe',
        type=int,
        help='Start frame to begin the clip',
        required=False)
    parser.add_argument(
        '-endframe',
        type=int,
        help='End frame',
        required=False)
    parser.add_argument(
        '-frames',
        nargs='+',
        type=int,
        help='List of frames to render',
        required=False)
    parser.add_argument(
        '-fps',
        type=int,
        help='FPS',
        required=False)
    parser.add_argument(
        '-resolution',
        nargs='+',
        type=int,
        help='Resolution X Y',
        required=False)
    parser.add_argument(
        '-colordepth',
        help='Color depth',
        required=False)
    parser.add_argument(
        '-colorspace',
        help='Footage colorspace',
        required=False)
    parser.add_argument(
        '-viewtransform',
        help='OCIO View Transform',
        required=False)
    parser.add_argument(
        '-output',
        help='File output',
        required=False)
    parser.add_argument(
        '-metadatas',
        nargs='+',
        required=False)
    parser.add_argument(
        '-codec',
        required=False)
    parser.add_argument(
        '-qscale',
        required=False)
    parser.add_argument(
        '-textoverlay',
        required=False)

    # remove Blender specific arguments from sys.argv
    # to be able to use argparse
    if '--' in sys.argv:
        index = sys.argv.index('--') + 1
        arguments = sys.argv[index:]
        args = parser.parse_args(arguments)
    else:
        args = parser.parse_args()

    return args
