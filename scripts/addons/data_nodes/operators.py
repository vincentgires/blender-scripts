import bpy
import mathutils
from .utils import update_nodes, AVAILABLE_NTREES
from operator import attrgetter

SOCKET_TYPE_ITEMS = (
    ('OUTPUT', 'Output', ''),
    ('INPUT', 'Input', ''))


class DataNodesUpdate(bpy.types.Operator):
    bl_idname = 'scene.update_data_node'
    bl_label = 'Update Nodes'
    bl_description = 'Force update data nodes'

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type in AVAILABLE_NTREES

    def execute(self, context):
        update_nodes()
        return {'FINISHED'}


class DataNodesGetObject(bpy.types.Operator):
    bl_idname = 'scene.get_object_to_data_node'
    bl_label = 'Get Object'
    bl_description = 'Get selected object from scene'

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type in AVAILABLE_NTREES

    def execute(self, context):
        node = context.node
        selected_object = context.object
        node.item = selected_object.name
        node.update()
        return {'FINISHED'}


class DataNodesRemoveSockets(bpy.types.Operator):
    bl_idname = 'scene.remove_sockets'
    bl_label = 'Remove Sockets'

    socket_type: bpy.props.EnumProperty(
        name='Socket Type',
        items=SOCKET_TYPE_ITEMS,
        default='OUTPUT')

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type in AVAILABLE_NTREES

    def execute(self, context):
        if hasattr(context, 'node'):
            node = context.node
        else:
            node = context.active_node
        if self.socket_type == 'OUTPUT':
            node.outputs.clear()
        elif self.socket_type == 'INPUT':
            node.inputs.clear()
        return {'FINISHED'}


class DataNodesRemoveSocket(bpy.types.Operator):
    bl_idname = 'scene.remove_socket'
    bl_label = 'Remove Socket'

    def _get_socket_items(self, context):
        node = context.active_node
        if self.socket_type == 'OUTPUT':
            sockets = node.outputs
        elif self.socket_type == 'INPUT':
            sockets = node.inputs
        return ((s.name, s.name, '') for s in sockets)

    socket_type: bpy.props.EnumProperty(
        name='Socket Type',
        items=SOCKET_TYPE_ITEMS,
        default='OUTPUT')
    socket: bpy.props.EnumProperty(
        items=_get_socket_items,
        name='Node Sockets')

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type in AVAILABLE_NTREES

    def execute(self, context):
        node = context.active_node
        if self.socket_type == 'OUTPUT':
            sockets = node.outputs
        elif self.socket_type == 'INPUT':
            sockets = node.inputs
        sockets.remove(sockets[self.socket])
        return {'FINISHED'}


class DataNodesRemoveInputSocket(DataNodesRemoveSocket):
    bl_idname = 'scene.remove_input_socket'
    bl_label = 'Remove Input Socket'
    socket_type: bpy.props.StringProperty(name='Socket Type', default='INPUT')


class DataNodesRemoveOutputSocket(DataNodesRemoveSocket):
    bl_idname = 'scene.remove_output_socket'
    bl_label = 'Remove Output Socket'
    socket_type: bpy.props.StringProperty(name='Socket Type', default='OUTPUT')


class DataNodesAddSocket(bpy.types.Operator):
    bl_idname = 'scene.add_socket_to_data_node'
    bl_label = 'Add Socket'
    bl_description = 'Add socket to the node'

    socket_type: bpy.props.EnumProperty(
        name='Socket Type',
        items=SOCKET_TYPE_ITEMS,
        default='OUTPUT')

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type in AVAILABLE_NTREES

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
            sockets = node.outputs
        elif self.socket_type == 'INPUT':
            sockets = node.inputs

        if node.attribute in sockets:
            return {'CANCELLED'}

        if isinstance(attribute, str):
            sockets.new('NodeSocketString', node.attribute)
        elif isinstance(attribute, bool):
            sockets.new('NodeSocketBool', node.attribute)
        elif isinstance(attribute, int):
            sockets.new('NodeSocketInt', node.attribute)
        elif isinstance(attribute, float):
            sockets.new('NodeSocketFloat', node.attribute)
        elif isinstance(attribute, mathutils.Color):
            sockets.new('NodeSocketColor', node.attribute)
        elif isinstance(attribute, vector_sockets):
            sockets.new('NodeSocketVector', node.attribute)
        elif len(attribute) == 4:  # RGBA
            sockets.new('NodeSocketColor', node.attribute)
        return {'FINISHED'}
