from bpy.types import Node
from ..utils import set_sockets


class IntToFloat(Node):
    """Int to float"""
    bl_idname = 'IntToFloatNodeType'
    bl_label = 'Int To Float'

    def init(self, context):
        self.inputs.new('NodeSocketInt', 'Int')
        self.outputs.new('NodeSocketFloat', 'Float')

    def update(self):
        value = self.inputs['Int'].default_value
        for output in self.outputs:
            set_sockets(output, float(value))

    def draw_label(self):
        return 'Int To Float'
