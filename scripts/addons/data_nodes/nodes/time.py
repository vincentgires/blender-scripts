import bpy
from bpy.types import NodeTree, Node, NodeSocket
from ..utils import send_value


class Time(Node):
    """Time node"""
    bl_idname = 'TimeNodeType'
    bl_label = 'Time info'

    def init(self, context):
        self.outputs.new('NodeSocketFloat', 'Frame')

    def update(self):
        send_value(self.outputs, bpy.context.scene.frame_current)

    def draw_label(self):
        return 'Time'
