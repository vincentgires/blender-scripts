import bpy
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.utils import send_value


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
                output = self.inputs['B'].default_value
            else:
                output = self.inputs['A'].default_value
            # Send data value to connected nodes
            send_value(self.outputs, output)

    def draw_label(self):
        return "Float Switch"
