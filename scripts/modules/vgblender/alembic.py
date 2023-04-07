import bpy
from .path import normpath


def load_objects_from_alembic(path, filter_type=None):
    context = bpy.context
    data = bpy.data
    current_scene = context.scene

    temporary_scene = data.scenes.new(name='Temp Scene')
    context.window.scene = temporary_scene
    bpy.ops.wm.alembic_import(filepath=normpath(path))
    if filter_type is None:
        objects = [ob for ob in temporary_scene.objects]
    else:
        objects = [ob for ob in temporary_scene.objects
                   if ob.type == filter_type]

    context.window.scene = current_scene
    data.scenes.remove(temporary_scene)
    return objects
