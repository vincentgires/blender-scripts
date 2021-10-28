import bpy
from bpy.types import Node
from ..utils import send_value


class FloatNumber(Node):
    """Float number node"""
    bl_idname = 'FloatNumberNodeType'
    bl_label = 'Float Number'

    def update_props(self, context):
        self.update()

    float_prop: bpy.props.FloatProperty(
        name='Float', default=1.0, update=update_props)

    def init(self, context):
        self.outputs.new('NodeSocketFloat', 'Float')

    def update(self):
        send_value(self.outputs, self.float_prop)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'float_prop')

    def draw_label(self):
        return 'Float number'
