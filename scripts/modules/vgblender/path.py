import os
import sys


def normpath(path):
    # remove double slash to be able to use it in Blender
    # result: /my/path
    if sys.platform.startswith('linux'):
        path = path.replace('//', '/')

    # make linux path compatible with windows
    # result after normpath: \\my\path
    elif sys.platform.startswith('win'):
        if path.startswith('/') and not path.startswith('//'):
            path = '/{}'.format(path)

    path = os.path.normpath(path)
    return path


def convert_os_path(path):
    if sys.platform.startswith('linux'):
        if path.startswith(r'\\'):
            path = '/' + path[2:]
    elif sys.platform.startswith('win'):
        if path.startswith('/') and not path.startswith('//'):
            path = r'\\' + path[1:]
    return path
