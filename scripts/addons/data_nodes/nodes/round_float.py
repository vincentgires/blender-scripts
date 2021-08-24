import bpy
from bpy.types import Node
from ..utils import send_value


class RoundFloat(Node):
    """Round float"""
    bl_idname = 'RoundFloatNodeType'
    bl_label = 'Round float'

    def init(self, context):
        self.inputs.new('NodeSocketFloat', 'Float')
        self.outputs.new('NodeSocketFloat', 'Float')
        self.outputs.new('NodeSocketInt', 'Int')

    def update(self):
        input_value = self.inputs['Float'].default_value
        input_value = round(input_value)
        send_value(self.outputs, input_value)

    def draw_label(self):
        return 'Round'
