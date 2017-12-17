import bpy
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.utils import send_value_link


class ColorSplit(Node):
    '''Color Split node'''
    bl_idname = 'ColorSplitNodeType'
    bl_label = 'Color Split'
    
    def init(self, context):
        self.inputs.new('NodeSocketColor', "Color")
        self.outputs.new('NodeSocketFloat', 'R')
        self.outputs.new('NodeSocketFloat', 'G')
        self.outputs.new('NodeSocketFloat', 'B')
        self.outputs.new('NodeSocketFloat', 'A')
    
    def update(self):
        
        # send data value to connected nodes
        for output in self.outputs:
            for link in output.links:
                
                if output.name == "R":
                    send_value_link(link, self.inputs["Color"].default_value[0])
                elif output.name == "G":
                    send_value_link(link, self.inputs["Color"].default_value[1])
                elif output.name == "B":
                    send_value_link(link, self.inputs["Color"].default_value[2])
                elif output.name == "A":
                    send_value_link(link, self.inputs["Color"].default_value[3])
    
    def draw_label(self):
        return "Color Split"
