import bpy
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.utils import send_value_link


class VectorSplit(Node):
    """Vector Split node"""
    bl_idname = 'VectorSplitNodeType'
    bl_label = 'Vector Split'

    def init(self, context):
        self.inputs.new('NodeSocketVector', 'Vector')
        self.outputs.new('NodeSocketFloat', 'X')
        self.outputs.new('NodeSocketFloat', 'Y')
        self.outputs.new('NodeSocketFloat', 'Z')

    def update(self):
        # Send data value to connected nodes
        for output in self.outputs:
            for link in output.links:
                if output.name == 'X':
                    send_value_link(
                        link, self.inputs['Vector'].default_value[0])
                elif output.name == 'Y':
                    send_value_link(
                        link, self.inputs['Vector'].default_value[1])
                elif output.name == 'Z':
                    send_value_link(
                        link, self.inputs['Vector'].default_value[2])

    def draw_label(self):
        return 'Vector Split'
