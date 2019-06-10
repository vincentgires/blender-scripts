import bpy
import mathutils
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.utils import send_value


class Vector(Node):
    """Vector node"""
    bl_idname = 'VectorNodeType'
    bl_label = 'Vector'

    def update_props(self, context):
        self.update()

    def init(self, context):
        self.inputs.new('NodeSocketFloat', 'X')
        self.inputs.new('NodeSocketFloat', 'Y')
        self.inputs.new('NodeSocketFloat', 'Z')
        self.outputs.new('NodeSocketVector', 'Vector')

    def update(self):
        if len(self.inputs) >= 3:
            # Send data value to connected nodes
            x = self.inputs["X"].default_value
            y = self.inputs["Y"].default_value
            z = self.inputs["Z"].default_value
            vector = mathutils.Vector((x, y, z))
            # Assign value to connected socket
            send_value(self.outputs, vector)

    def draw_label(self):
        return 'Vector'
