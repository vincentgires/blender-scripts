import bpy
from bpy.types import NodeTree, Node, NodeSocket
from ..utils import send_value


class Color(Node):
    """Color node"""
    bl_idname = 'ColorNodeType'
    bl_label = 'Color'

    def update_props(self, context):
        self.update()

    color_prop = bpy.props.FloatVectorProperty(
        name='Color',
        subtype='COLOR',
        size=4,  # 4 = RGBA
        soft_min=0.0, soft_max=1.0,
        default=(1, 1, 1, 1),
        update=update_props)

    def init(self, context):
        self.outputs.new('NodeSocketColor', 'Color')

    def update(self):
        send_value(self.outputs, self.color_prop)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'color_prop')

    def draw_label(self):
        return 'Color'
