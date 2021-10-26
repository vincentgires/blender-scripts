import bpy
import mathutils
from .utils import update_nodes
from operator import attrgetter


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
        update_nodes()
        return {'FINISHED'}


class DataNodesGetObject(bpy.types.Operator):
    bl_idname = 'scene.get_object_to_data_node'
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
        node.item = selected_object.name
        node.update()
        return {'FINISHED'}


class DataNodesRemoveSockets(bpy.types.Operator):
    bl_idname = 'scene.remove_sockets'
    bl_label = 'Remove input sockets'
    bl_description = 'Remove input sockets'

    socket_type: bpy.props.EnumProperty(
        name='Socket type',
        items=(('OUTPUT', 'output', ''),
               ('INPUT', 'input', '')),
        default='OUTPUT')

    def execute(self, context):
        node = context.node
        if self.socket_type == 'OUTPUT':
            node.outputs.clear()
        elif self.socket_type == 'INPUT':
            node.inputs.clear()
        return {'FINISHED'}


class DataNodesAddSocket(bpy.types.Operator):
    bl_idname = 'scene.add_socket_to_data_node'
    bl_label = 'Add socket'
    bl_description = 'Add socket to the node'

    socket_type: bpy.props.EnumProperty(
        name='Socket type',
        items=(('OUTPUT', 'output', ''),
               ('INPUT', 'input', '')),
        default='OUTPUT')

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree and context.node.attribute

    def execute(self, context):
        node = context.node
        if not node.item:
            return

        data_collection = getattr(bpy.data, node.data)
        item = data_collection.get(node.item)

        if item is None:
            return {'CANCELLED'}

        attribute = attrgetter(node.attribute)(item)
        vector_sockets = (mathutils.Vector, mathutils.Euler, mathutils.Euler)
        if self.socket_type == 'OUTPUT':
            socket = node.outputs
        elif self.socket_type == 'INPUT':
            socket = node.inputs

        if isinstance(attribute, str):
            socket.new('NodeSocketString', node.attribute)
        elif isinstance(attribute, bool):
            socket.new('NodeSocketBool', node.attribute)
        elif isinstance(attribute, int):
            socket.new('NodeSocketInt', node.attribute)
        elif isinstance(attribute, float):
            socket.new('NodeSocketFloat', node.attribute)
        elif isinstance(attribute, mathutils.Color):
            socket.new('NodeSocketColor', node.attribute)
        elif isinstance(attribute, vector_sockets):
            socket.new('NodeSocketVector', node.attribute)
        elif len(attribute) == 4:  # RGBA
            socket.new('NodeSocketColor', node.attribute)
        return {'FINISHED'}
