import os
import sys
import bpy
from bpy.app.handlers import persistent
from vgblender.path import normpath

filepath = normpath(sys.argv[-1])


def load_file_as_image():
    if not os.path.exists(filepath):
        return
    scene = bpy.context.scene
    image = bpy.data.images.load(filepath)
    image.use_view_as_render = True
    screen = bpy.context.screen
    for area in screen.areas:
        if area.type == 'IMAGE_EDITOR':
            space = area.spaces.active
            space.image = image


@persistent
def load_handler(dummy):
    load_file_as_image()


def register():
    bpy.app.handlers.load_factory_startup_post.append(load_handler)


def unregister():
    bpy.app.handlers.load_factory_startup_post.remove(load_handler)
