import bpy
from bpy.types import NodeTree
from bpy.props import StringProperty, CollectionProperty, FloatVectorProperty
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem
from .nodes import (
    boolean, color, color_combine, color_palette, color_split, condition,
    data_input, data_output, debug, distance, expression, float_number,
    float_switch, float_to_int, float_to_string, integer, int_to_float, note,
    object_properties, render, render_engine, view_layer, round_float, time,
    vector_split, vector, NODES_TYPES)
from . import operators
from .utils import (
    frame_change, scene_update, render_pre_update, render_post_update)


bl_info = {
    'name': 'Data Nodes',
    'author': 'Vincent Girès',
    'description': (
        'Node utils for Cycles, the compositor'
        'and a custom Data Node Tree'),
    'version': (0, 0, 3),
    'blender': (2, 80, 0),
    'location': 'Node Editor',
    'category': 'Node'}


class ColorPaletteColorProperty(bpy.types.PropertyGroup):
    color: FloatVectorProperty(
        name='Color',
        subtype='COLOR',
        size=4,
        soft_min=0.0, soft_max=1.0,
        default=(0.5, 0.5, 0.5, 1.0))


class ColorPaletteCollectionProperty(bpy.types.PropertyGroup):
    name: StringProperty(name='Color Palette name', default='Palette')
    color_collection: CollectionProperty(type=ColorPaletteColorProperty)


class NodeEditorDataTree(NodeTree):
    bl_idname = 'DataNodeTree'
    bl_label = 'Data Node Tree'
    bl_icon = 'NODETREE'


class NodeEditorDataNodesPanel(bpy.types.Panel):
    bl_idname = 'DATANODES_PT_node_editor'
    bl_label = 'Tools'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Data'

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree

    def draw(self, context):
        layout = self.layout
        layout.operator('update_data_node.btn', icon='FILE_REFRESH')


class DataNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree


classes = (
    operators.DataNodesUpdate,
    operators.DataNodesGetObject,
    operators.DataNodesRemoveInputSockets,
    operators.DataNodesRemoveOutputSockets,
    operators.DataNodesAddOutputSocket,
    operators.DataNodesAddInputSocket,
    boolean.Boolean,
    color.Color,
    color_combine.ColorCombine,
    color_palette.TemplateColorPaletteCollectionUL,
    color_palette.ColorPalette,
    color_palette.CustomNodesAddPaletteItem,
    color_palette.CustomNodesRemovePaletteItem,
    color_palette.CustomNodesAddPaletteColor,
    color_palette.CustomNodesRemovePaletteColor,
    color_palette.CustomNodesClearPaletteColor,
    color_split.ColorSplit,
    condition.Condition,
    data_input.DataInputNode,
    data_output.DataOutputNode,
    debug.DebugNode,
    distance.DistanceNode,
    expression.Expression,
    expression.ExpressionNodeAddInputSocket,
    float_number.FloatNumber,
    float_switch.FloatSwitch,
    float_to_int.FloatToInt,
    float_to_string.FloatToString,
    integer.Integer,
    int_to_float.IntToFloat,
    note.NoteNode,
    object_properties.ObjectPropertiesNode,
    render.RenderNode,
    render_engine.RenderEngineNode,
    view_layer.ViewLayerNode,
    round_float.RoundFloat,
    time.Time,
    vector.Vector,
    vector_split.VectorSplit,
    ColorPaletteColorProperty,
    ColorPaletteCollectionProperty,
    NodeEditorDataTree,
    NodeEditorDataNodesPanel
)

node_categories = [
    # identifier, label, items list
    DataNodeCategory(
        'DATA', 'Data', items=[NodeItem(n) for n in NODES_TYPES])]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    nodeitems_utils.register_node_categories('NODE_UTILS', node_categories)
    bpy.types.Scene.colorpalette_collection = CollectionProperty(
        type=ColorPaletteCollectionProperty)

    bpy.app.handlers.frame_change_post.append(frame_change)
    bpy.app.handlers.depsgraph_update_post.append(scene_update)
    bpy.app.handlers.render_pre.append(render_pre_update)
    bpy.app.handlers.render_post.append(render_post_update)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    nodeitems_utils.unregister_node_categories('NODE_UTILS')
    del bpy.types.Scene.colorpalette_collection

    bpy.app.handlers.frame_change_post.remove(frame_change)
    bpy.app.handlers.depsgraph_update_post.remove(scene_update)
    bpy.app.handlers.render_pre.remove(render_pre_update)
    bpy.app.handlers.render_post.remove(render_post_update)


if __name__ == '__main__':
    register()
