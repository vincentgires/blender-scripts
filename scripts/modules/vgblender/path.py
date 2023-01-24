import os
import sys
import bpy


def normpath(path):
    """Set path to correct OS and Blender convention"""

    # Remove double slash to be able to use it in Blender
    if sys.platform.startswith('linux'):
        path = path.replace('//', '/')
    # Result: /my/path

    # Make linux path compatible with windows
    elif sys.platform.startswith('win'):
        if path.startswith('/') and not path.startswith('//'):
            path = '/{}'.format(path)
    # Result after normpath: \\my\path

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


def conform_data_paths():
    """Adapt paths for Linux or Windows"""

    for scene in bpy.data.scenes:
        scene.render.filepath = convert_os_path(scene.render.filepath)
        if not scene.sequence_editor:
            continue
        sequences = scene.sequence_editor.sequences_all
        for strip in sequences:
            match strip.type:
                case 'MOVIE':
                    strip.filepath = convert_os_path(strip.filepath)
                case 'IMAGE':
                    strip.directory = convert_os_path(strip.directory)
    for image in bpy.data.images:
        image.filepath = convert_os_path(image.filepath)
