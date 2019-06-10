import bpy
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.utils import send_value


class IntToFloat(Node):
    """Int to float"""
    bl_idname = 'IntToFloatNodeType'
    bl_label = 'Int To Float'

    def init(self, context):
        self.inputs.new('NodeSocketInt', 'Int')
        self.outputs.new('NodeSocketFloat', 'Float')

    def update(self):
        input_value = self.inputs['Int'].default_value
        input_value = float(input_value)
        # Send data value to connected nodes
        send_value(self.outputs, input_value)

    def draw_label(self):
        return 'Int to float'
