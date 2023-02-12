import bpy
from bpy.types import Node
from ..utils import set_sockets


class Time(Node):
    """Time node"""
    bl_idname = 'TimeNodeType'
    bl_label = 'Time Info'

    def init(self, context):
        self.outputs.new('NodeSocketFloat', 'Frame')

    def update(self):
        for output in self.outputs:
            set_sockets(output, bpy.context.scene.frame_current)

    def draw_label(self):
        return 'Time'
