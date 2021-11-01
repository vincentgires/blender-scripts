import bpy
import mathutils
from bpy.types import Node
from ..utils import set_sockets


class Vector(Node):
    """Vector node"""
    bl_idname = 'VectorNodeType'
    bl_label = 'Vector'

    def update_props(self, context):
        self.update()

    def init(self, context):
        for socket_name in ('X', 'Y', 'Z'):
            self.inputs.new('NodeSocketFloat', socket_name)
        self.outputs.new('NodeSocketVector', 'Vector')

    def update(self):
        if len(self.inputs) >= 3:
            x, y, z = (self.inputs[i].default_value for i in ('X', 'Y', 'Z'))
            vector = mathutils.Vector((x, y, z))
            for output in self.outputs:
                set_sockets(output, vector)

    def draw_label(self):
        return 'Vector'
