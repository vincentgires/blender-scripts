import bpy
from bpy.types import Node
from ..utils import set_sockets


class FloatToInt(Node):
    """Float To String node"""
    bl_idname = 'FloatToIntNodeType'
    bl_label = 'Float To Int'

    def init(self, context):
        self.inputs.new('NodeSocketFloat', 'Float')
        self.outputs.new('NodeSocketInt', 'Int')

    def update(self):
        value = int(round(self.inputs['Float'].default_value))
        for output in self.outputs:
            set_sockets(output, value)

    def draw_label(self):
        return 'Float To Int'
