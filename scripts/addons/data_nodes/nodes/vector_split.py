import bpy
from bpy.types import Node
from ..utils import set_sockets


class VectorSplit(Node):
    """Vector Split node"""
    bl_idname = 'VectorSplitNodeType'
    bl_label = 'Vector Split'

    def init(self, context):
        self.inputs.new('NodeSocketVector', 'Vector')
        for socket_name in ('X', 'Y', 'Z'):
            self.outputs.new('NodeSocketFloat', socket_name)

    def update(self):
        for output in self.outputs:
            if output.name == 'X':
                set_sockets(output, self.inputs['Vector'].default_value[0])
            elif output.name == 'Y':
                set_sockets(output, self.inputs['Vector'].default_value[1])
            elif output.name == 'Z':
                set_sockets(output, self.inputs['Vector'].default_value[2])

    def draw_label(self):
        return 'Vector Split'
