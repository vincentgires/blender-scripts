import bpy
from bpy.types import Node
from ..utils import send_value


class FloatToString(Node):
    """Float To String node"""
    bl_idname = 'FloatToStringNodeType'
    bl_label = 'Float To String'

    def update_props(self, context):
        self.update()

    value: bpy.props.BoolProperty(
        name='Round', update=update_props)

    def init(self, context):
        self.inputs.new('NodeSocketFloat', 'Float')
        self.outputs.new('NodeSocketString', 'String')

    def update(self):
        input_value = self.inputs['Float'].default_value
        if self.value:
            input_value = round(input_value)
        input_value = str(input_value)
        # Send data value to connected nodes
        send_value(self.outputs, input_value)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'value')

    def draw_label(self):
        return 'Float To String'
