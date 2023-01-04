import bpy
import json
from . import gldraw
from .core import add_text
from vgblender.area import redraw_area
from vgblender.datautils import remove_item_from_collection


class TitleAddText(bpy.types.Operator):
    bl_idname = 'scene.title_add_text'
    bl_label = 'Add text'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        sequence_editor = scene.sequence_editor
        strip = sequence_editor.active_strip
        add_text(strip)
        return {'FINISHED'}


class TitleRemoveText(bpy.types.Operator):
    """Remove note"""
    bl_idname = 'scene.title_remove_text'
    bl_label = 'Remove text'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        sequence_editor = scene.sequence_editor
        strip = sequence_editor.active_strip
        index = strip.active_text_index
        text = strip.texts[index]
        remove_item_from_collection(
            strip.texts,
            strip, 'active_text_index')
        redraw_area(context)
        return {'FINISHED'}
