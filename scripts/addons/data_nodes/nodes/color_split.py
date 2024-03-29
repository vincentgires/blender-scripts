from bpy.types import Node
from ..utils import set_sockets


class ColorSplit(Node):
    """Color Split node"""
    bl_idname = 'ColorSplitNodeType'
    bl_label = 'Color Split'

    def init(self, context):
        self.inputs.new('NodeSocketColor', 'Color')
        for socket_name in ('R', 'G', 'B', 'A'):
            self.outputs.new('NodeSocketFloat', socket_name)

    def update(self):
        for output in self.outputs:
            if output.name == 'R':
                set_sockets(output, self.inputs['Color'].default_value[0])
            elif output.name == 'G':
                set_sockets(output, self.inputs['Color'].default_value[1])
            elif output.name == 'B':
                set_sockets(output, self.inputs['Color'].default_value[2])
            elif output.name == 'A':
                set_sockets(output, self.inputs['Color'].default_value[3])

    def draw_label(self):
        return 'Color Split'
