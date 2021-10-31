import bpy
from bpy.types import Node
from ..utils import set_sockets


class FloatToString(Node):
    """Float To String node"""
    bl_idname = 'FloatToStringNodeType'
    bl_label = 'Float To String'

    def update_props(self, context):
        self.update()

    round: bpy.props.BoolProperty(
        name='Round', update=update_props)

    def init(self, context):
        self.inputs.new('NodeSocketFloat', 'Float')
        self.outputs.new('NodeSocketString', 'String')

    def update(self):
        value = self.inputs['Float'].default_value
        if self.round:
            value = round(value)
        for output in self.outputs:
            set_sockets(output, str(value))

    def draw_buttons(self, context, layout):
        layout.prop(self, 'value')

    def draw_label(self):
        return 'Float To String'
