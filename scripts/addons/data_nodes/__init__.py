import bpy
from bpy.types import NodeTree
from bpy.props import StringProperty, CollectionProperty, FloatVectorProperty
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem
from .nodes import (
    boolean, color, color_combine, color_palette, color_split, condition,
    data_input, data_output, debug, distance, expression, float_number,
    float_switch, float_to_int, float_to_string, integer, int_to_float, note,
    object_properties, render, render_engine, round_float, scene, time,
    vector_split, vector, view_layer, NODES_TYPES)
from . import operators
from .utils import (
    frame_change, scene_update, render_pre_update, render_post_update,
    AVAILABLE_NTREES)


bl_info = {
    'name': 'Data Nodes',
    'author': 'Vincent Girès',
    'description': (
        'Node utils for shading network, the compositor '
        'and a custom Data Node Tree'),
    'version': (0, 0, 3),
    'blender': (5, 1, 0),
    'location': 'Node Editor',
    'category': 'Node'}


class ColorPaletteColorProperty(bpy.types.PropertyGroup):
    color: FloatVectorProperty(
        name='Color',
        subtype='COLOR',
        size=4,  # RGBA
        soft_min=0.0, soft_max=1.0,
        default=(0.5, 0.5, 0.5, 1.0))


class ColorPaletteProperties(bpy.types.PropertyGroup):
    name: StringProperty(name='Color Palette name', default='Palette')
    colors: CollectionProperty(type=ColorPaletteColorProperty)


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
        return context.space_data.tree_type in AVAILABLE_NTREES

    def draw(self, context):
        layout = self.layout
        layout.operator('scene.update_data_node', icon='FILE_REFRESH')


class SocketsPanel(bpy.types.Panel):
    bl_idname = 'DATANODES_PT_sockets'
    bl_label = 'Sockets'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Data'

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type in AVAILABLE_NTREES

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        fac = 0.3
        sub = col.split(factor=fac)
        sub.label(text='Remove')
        sub.operator_menu_enum(
            'scene.remove_input_socket', 'socket', text='Input')
        sub = col.split(factor=fac)
        sub.separator()
        sub.operator_menu_enum(
            'scene.remove_output_socket', 'socket', text='Output')
        col = layout.column(align=True)
        sub = col.split(factor=fac)
        sub.label(text='Clear')
        input_op = sub.operator('scene.remove_sockets', text='Input')
        input_op.socket_type = 'INPUT'
        sub = col.split(factor=fac)
        sub.separator()
        output_op = sub.operator('scene.remove_sockets', text='Output')
        output_op.socket_type = 'OUTPUT'


class DataNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type in AVAILABLE_NTREES


node_classes = [
    boolean.Boolean,
    color.Color,
    color_combine.ColorCombine,
    color_palette.ColorPalette,
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
    scene.SceneNode,
    time.Time,
    vector.Vector,
    vector_split.VectorSplit]

menu_label = 'Data'
tree_types = ['CompositorNodeTree', 'ShaderNodeTree', 'GeometryNodeTree']

class AddCustomNode(bpy.types.Operator):
    bl_idname = 'node.add_custom_node'
    bl_label = 'Add Custom Node'

    node_type: bpy.props.StringProperty()

    def execute(self, context):
        tree = context.space_data.node_tree
        tree.nodes.new(self.node_type)
        return {'FINISHED'}

class CustomSubmenu(bpy.types.Menu):
    bl_label = menu_label
    bl_idname = 'DATANODES_MT_custom_submenu'

    def draw(self, context):
        layout = self.layout
        for node_class in node_classes:
            op = layout.operator(
                'node.add_custom_node',
                text=node_class.bl_label)
            op.node_type = node_class.bl_idname


def draw_custom_nodes(self, context):
    if context.space_data.tree_type not in tree_types:
        return
    layout = self.layout
    layout.separator()
    layout.menu('DATANODES_MT_custom_submenu', icon='NODE')


classes = node_classes + [
    operators.DataNodesUpdate,
    operators.DataNodesGetObject,
    operators.DataNodesRemoveSockets,
    operators.DataNodesRemoveSocket,
    operators.DataNodesRemoveInputSocket,
    operators.DataNodesRemoveOutputSocket,
    operators.DataNodesAddSocket,
    color_palette.TemplateColorPaletteCollectionUL,
    color_palette.ColorPaletteAdd,
    color_palette.ColorPaletteRemove,
    color_palette.ColorPaletteAddColor,
    color_palette.ColorPaletteRemoveColor,
    ColorPaletteColorProperty,
    ColorPaletteProperties,
    NodeEditorDataTree,
    NodeEditorDataNodesPanel,
    SocketsPanel]

node_categories = [
    # identifier, label, items list
    DataNodeCategory('DATA', 'Data', items=[NodeItem(n) for n in NODES_TYPES])]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    nodeitems_utils.register_node_categories('DATA_NODES', node_categories)
    bpy.types.Scene.color_palettes = CollectionProperty(
        type=ColorPaletteProperties)

    bpy.utils.register_class(AddCustomNode)
    bpy.utils.register_class(CustomSubmenu)
    bpy.types.NODE_MT_add.append(draw_custom_nodes)

    bpy.app.handlers.frame_change_post.append(frame_change)
    bpy.app.handlers.depsgraph_update_post.append(scene_update)
    bpy.app.handlers.render_pre.append(render_pre_update)
    bpy.app.handlers.render_post.append(render_post_update)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    nodeitems_utils.unregister_node_categories('DATA_NODES')
    del bpy.types.Scene.color_palettes

    bpy.types.NODE_MT_add.remove(draw_custom_nodes)
    bpy.utils.unregister_class(CustomSubmenu)
    bpy.utils.unregister_class(AddCustomNode)

    bpy.app.handlers.frame_change_post.remove(frame_change)
    bpy.app.handlers.depsgraph_update_post.remove(scene_update)
    bpy.app.handlers.render_pre.remove(render_pre_update)
    bpy.app.handlers.render_post.remove(render_post_update)


if __name__ == '__main__':
    register()
