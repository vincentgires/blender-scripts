import bpy
from bpy.types import PropertyGroup, SpaceSequenceEditor, Scene, Sequence
from bpy.props import (
    StringProperty, IntProperty, FloatVectorProperty, BoolProperty,
    CollectionProperty)
import os
from . import ui, operators, gldraw


bl_info = {
    'name': 'Title',
    'author': 'Vincent Girès',
    'description': 'Title overlay for the sequencer',
    'version': (0, 0, 1),
    'blender': (2, 80, 0),
    'location': 'Sequenter properties panel',
    'category': 'Sequencer'}


class TextItemProperties(PropertyGroup):
    name: StringProperty(
        name='Name',
        default='Text')
    color: FloatVectorProperty(
        name='Color',
        subtype='COLOR',
        size=4,
        soft_min=0.0,
        soft_max=1.0,
        default=(1.0, 0.0, 0.0, 1.0))
    position: FloatVectorProperty(
        name='Position',
        subtype='XYZ',
        size=2,
        soft_min=0.0,
        soft_max=1.0,
        step=0.25,
        default=(0.5, 0.5))
    size: IntProperty(
        name='Size',
        soft_min=0,
        soft_max=100,
        default=35)
    display: BoolProperty(
        name='Display',
        default=True)
    # TODO
    # font: StringProperty(
    #     name='Font',
    #     default='')


classes = [
    TextItemProperties,
    operators.TitleAddText,
    operators.TitleRemoveText,
    ui.TextsUL,
    ui.TitlePanel]
draw_handler = {}


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    Sequence.active_text_index = bpy.props.IntProperty(
        name='Active text index',
        default=0,
        min=0)
    Sequence.texts = CollectionProperty(type=TextItemProperties)
    draw_handler['text'] = SpaceSequenceEditor.draw_handler_add(
        gldraw.draw_texts, (), 'PREVIEW', 'POST_PIXEL')


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del Sequence.active_text_index
    del Sequence.texts
    SpaceSequenceEditor.draw_handler_remove(
        draw_handler['text'], 'PREVIEW')
