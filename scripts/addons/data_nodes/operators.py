import bpy
import math
import mathutils
from .utils import update_nodes


class DataNodesUpdate(bpy.types.Operator):
    bl_idname = 'update_data_node.btn'
    bl_label = 'Update nodes'
    bl_description = 'Force update data nodes'

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree

    def execute(self, context):
        selected_nodes = context.selected_nodes
        active_node = context.active_node
        update_nodes(context.scene)
        return {'FINISHED'}


class DataNodesGetObject(bpy.types.Operator):
    bl_idname = 'get_object_to_data_node.btn'
    bl_label = 'Get object'
    bl_description = 'Get selected object from scene'

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree

    def execute(self, context):
        node = context.node
        selected_object = context.object
        node.data_item = selected_object.name
        return {'FINISHED'}


class DataNodesRemoveInputSockets(bpy.types.Operator):
    bl_idname = 'remove_input_sockets.btn'
    bl_label = 'Remove input sockets'
    bl_description = 'Remove input sockets'

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node = context.node
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree and node.inputs

    def execute(self, context):
        node = context.node
        selected_object = context.object
        node.inputs.clear()
        return {'FINISHED'}


class DataNodesRemoveOutputSockets(bpy.types.Operator):
    bl_idname = 'remove_output_sockets.btn'
    bl_label = 'Remove output sockets'
    bl_description = 'Remove output sockets'

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node = context.node
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree and node.outputs

    def execute(self, context):
        node = context.node
        selected_object = context.object
        node.outputs.clear()
        return {'FINISHED'}


class DataNodesAddOutputSocket(bpy.types.Operator):
    bl_idname = 'add_output_socket_to_data_node.btn'
    bl_label = 'Add output socket'
    bl_description = 'Add output socket to the node'

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree and context.node.attribute_property

    def execute(self, context):
        node = context.node
        selected_object = context.object

        # get attribute value and type
        data_path = 'bpy.data.' + node.data_enum + '["' + node.data_item + '"]'
        data_path = eval(data_path)
        try:
            attribute = eval('data_path.' + node.attribute_property)
        except:
            attribute = None

        if attribute is not None:
            if isinstance(attribute, str):
                node.outputs.new('NodeSocketString', node.attribute_property)
            elif isinstance(attribute, bool):
                node.outputs.new('NodeSocketBool', node.attribute_property)
            elif isinstance(attribute, int):
                node.outputs.new('NodeSocketInt', node.attribute_property)
            elif isinstance(attribute, float):
                node.outputs.new('NodeSocketFloat', node.attribute_property)
            elif isinstance(attribute, mathutils.Color):
                node.outputs.new('NodeSocketColor', node.attribute_property)
            elif isinstance(attribute, mathutils.Vector):
                node.outputs.new('NodeSocketVector', node.attribute_property)
            elif isinstance(attribute, mathutils.Euler):
                node.outputs.new('NodeSocketVector', node.attribute_property)
            elif isinstance(attribute, mathutils.Quaternion):
                node.outputs.new('NodeSocketVector', node.attribute_property)
            elif len(attribute) == 4:  # RGBA
                node.outputs.new('NodeSocketColor', node.attribute_property)

        return {'FINISHED'}


class DataNodesAddInputSocket(bpy.types.Operator):
    bl_idname = 'add_input_socket_to_data_node.btn'
    bl_label = 'Add input socket'
    bl_description = 'Add input socket to the node'

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree and context.node.attribute_property

    def execute(self, context):
        node = context.node
        selected_object = context.object

        # get attribute value and type
        data_path = 'bpy.data.' + node.data_enum + '["' + node.data_item + '"]'
        data_path = eval(data_path)
        try:
            attribute = eval('data_path.' + node.attribute_property)
        except:
            attribute = None

        if attribute is not None:
            if isinstance(attribute, str):
                node.inputs.new('NodeSocketString', node.attribute_property)
            elif isinstance(attribute, bool):
                node.inputs.new('NodeSocketBool', node.attribute_property)
            elif isinstance(attribute, int):
                node.inputs.new('NodeSocketInt', node.attribute_property)
            elif isinstance(attribute, float):
                node.inputs.new('NodeSocketFloat', node.attribute_property)
            elif isinstance(attribute, mathutils.Color):
                node.inputs.new('NodeSocketColor', node.attribute_property)
            elif isinstance(attribute, mathutils.Vector):
                node.inputs.new('NodeSocketVector', node.attribute_property)
            elif isinstance(attribute, mathutils.Euler):
                node.inputs.new('NodeSocketVector', node.attribute_property)
            elif isinstance(attribute, mathutils.Quaternion):
                node.inputs.new('NodeSocketVector', node.attribute_property)
            elif len(attribute) == 4:  # RGBA
                node.inputs.new('NodeSocketColor', node.attribute_property)

        return {'FINISHED'}
