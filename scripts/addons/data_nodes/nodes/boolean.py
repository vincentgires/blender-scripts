import bpy
from bpy.types import Node
from ..utils import send_value


class Boolean(Node):
    """Boolean node"""
    bl_idname = 'BooleanNodeType'
    bl_label = 'Boolean'

    def update_props(self, context):
        self.update()

    value: bpy.props.BoolProperty(
        name='Bool',
        default=True,
        update=update_props)

    def init(self, context):
        self.outputs.new('NodeSocketBool', 'Boolean')

    def update(self):
        send_value(self.outputs, self.value)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'value')

    def draw_label(self):
        return 'Boolean'
