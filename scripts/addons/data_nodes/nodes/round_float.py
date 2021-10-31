import bpy
from bpy.types import Node
from ..utils import set_sockets


class RoundFloat(Node):
    """Round float"""
    bl_idname = 'RoundFloatNodeType'
    bl_label = 'Round float'

    def init(self, context):
        self.inputs.new('NodeSocketFloat', 'Float')
        self.outputs.new('NodeSocketFloat', 'Float')
        self.outputs.new('NodeSocketInt', 'Int')

    def update(self):
        value = round(self.inputs['Float'].default_value)
        for output in self.outputs:
            set_sockets(output, value)

    def draw_label(self):
        return 'Round'
