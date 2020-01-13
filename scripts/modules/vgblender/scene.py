import bpy
from . import argconfig
from .render.metadata import set_metadata_overlay


def set_scene_from_args(scene):
    args = argconfig.get_args()
    if args.fps:
        scene.render.fps = args.fps
    if args.resolution:
        x, y = args.resolution
        scene.render.resolution_x = x
        scene.render.resolution_y = y
    if args.viewtransform:
        scene.view_settings.view_transform = args.viewtransform
    if args.colordepth:
        scene.render.image_settings.color_depth = args.colordepth
    if args.output:
        scene.render.filepath = args.output
    if args.textoverlay:
        set_metadata_overlay(scene, note=args.textoverlay)
