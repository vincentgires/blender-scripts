import bpy
from bpy.types import Node
from ..utils import set_sockets


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
        for output in self.outputs:
            set_sockets(output, self.value)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'value')

    def draw_label(self):
        return 'Boolean'
