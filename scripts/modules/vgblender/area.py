import bpy


def redraw_area(context, area_types=None):
    if area_types is None:
        context.area.tag_redraw()
        return
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type in area_types:
                area.tag_redraw()
