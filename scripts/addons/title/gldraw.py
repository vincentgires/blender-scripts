import bpy
import bgl
import blf
import json
from vgblender.glutils import draw_text
from vgblender.sequencer import get_current_strips, view_zoom_preview


def draw_texts():
    context = bpy.context
    scene = context.scene
    view2d = context.region.view2d

    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y

    orig_x, orig_y = view2d.view_to_region(0.0, 0.0, clip=False)
    orig_x -= (res_x / 2) / view_zoom_preview(context)
    orig_y -= (res_y / 2) / view_zoom_preview(context)

    for strip in get_current_strips(scene):
        for text in strip.texts:
            if not text.display:
                continue
            x = orig_x \
                + (text.position.x * scene.render.resolution_x) \
                / view_zoom_preview(context)
            y = orig_y \
                + (text.position.y * scene.render.resolution_y) \
                / view_zoom_preview(context)
            size = int(text.size / view_zoom_preview(context))
            position = (x, y, 0)
            draw_text(text.name, position, text.color, size)
