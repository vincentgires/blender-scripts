import bpy
from bpy.types import Node
from ..utils import set_sockets


class RenderNode(Node):
    """Render node"""
    bl_idname = 'RenderNodeType'
    bl_label = 'Render'

    on_render: bpy.props.FloatProperty(
        name='On render', default=0)

    def init(self, context):
        self.outputs.new('NodeSocketFloat', 'On Render')

    def update(self):
        for output in self.outputs:
            set_sockets(output, self.on_render)

    def draw_label(self):
        return 'Render'
