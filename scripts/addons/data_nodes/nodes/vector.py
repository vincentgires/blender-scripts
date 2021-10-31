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
        self.inputs.new('NodeSocketFloat', 'X')
        self.inputs.new('NodeSocketFloat', 'Y')
        self.inputs.new('NodeSocketFloat', 'Z')
        self.outputs.new('NodeSocketVector', 'Vector')

    def update(self):
        if len(self.inputs) >= 3:
            x = self.inputs['X'].default_value
            y = self.inputs['Y'].default_value
            z = self.inputs['Z'].default_value
            vector = mathutils.Vector((x, y, z))
            for output in self.outputs:
                set_sockets(output, vector)

    def draw_label(self):
        return 'Vector'
