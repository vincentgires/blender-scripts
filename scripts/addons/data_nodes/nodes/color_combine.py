import mathutils
from bpy.types import Node
from ..utils import set_sockets


class ColorCombine(Node):
    """Color Split node"""
    bl_idname = 'ColorCombineNodeType'
    bl_label = 'Color Combine'

    def init(self, context):
        for socket_name in ('R', 'G', 'B', 'A'):
            self.inputs.new('NodeSocketFloat', socket_name)
        self.outputs.new('NodeSocketColor', 'Color')

    def update(self):
        if len(self.inputs) >= 4:
            color = mathutils.Vector((0.0, 0.0, 0.0, 0.0))
            color[0] = self.inputs[0].default_value
            color[1] = self.inputs[1].default_value
            color[2] = self.inputs[2].default_value
            color[3] = self.inputs[3].default_value
            for output in self.outputs:
                set_sockets(output, color)

    def draw_label(self):
        return 'Color Combine'
