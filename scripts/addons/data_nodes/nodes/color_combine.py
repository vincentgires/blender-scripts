import bpy
import mathutils
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.utils import send_value


class ColorCombine(Node):
    """Color Split node"""
    bl_idname = 'ColorCombineNodeType'
    bl_label = 'Color Combine'

    def init(self, context):
        self.inputs.new('NodeSocketFloat', 'R')
        self.inputs.new('NodeSocketFloat', 'G')
        self.inputs.new('NodeSocketFloat', 'B')
        self.inputs.new('NodeSocketFloat', 'A')
        self.outputs.new('NodeSocketColor', 'Color')

    def update(self):
        if len(self.inputs) >= 4:
            color = mathutils.Vector((0.0, 0.0, 0.0, 0.0))
            color[0] = self.inputs[0].default_value
            color[1] = self.inputs[1].default_value
            color[2] = self.inputs[2].default_value
            color[3] = self.inputs[3].default_value
            send_value(self.outputs, color)

    def draw_label(self):
        return 'Color Combine'
