import bpy
from bpy.types import Node
from ..utils import set_sockets


class FloatSwitch(Node):
    """Float To String node"""
    bl_idname = 'FloatSwitchNodeType'
    bl_label = 'Float Switch'

    def init(self, context):
        self.inputs.new('NodeSocketFloat', 'A')
        self.inputs.new('NodeSocketFloat', 'B')
        self.inputs.new('NodeSocketFloat', 'Switch')
        self.outputs.new('NodeSocketFloat', 'Value')

    def update(self):
        if len(self.inputs) >= 3:
            if self.inputs['Switch'].default_value > 0.0:
                value = self.inputs['B'].default_value
            else:
                value = self.inputs['A'].default_value
            for output in self.outputs:
                set_sockets(output, value)

    def draw_label(self):
        return 'Float Switch'
