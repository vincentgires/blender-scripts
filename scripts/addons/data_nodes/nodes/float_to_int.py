import bpy
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.utils import send_value


class FloatToInt(Node):
    '''Float To String node'''
    bl_idname = 'FloatToIntNodeType'
    bl_label = 'Float To Int'
    
    def init(self, context):
        self.inputs.new('NodeSocketFloat', "Float")
        self.outputs.new('NodeSocketInt', "Int")
    
    def update(self):
        input_value = self.inputs["Float"].default_value
        input_value = round(input_value)
        input_value = int(input_value)
        
        # send data value to connected nodes
        send_value(self.outputs, input_value)
    
    def draw_label(self):
        return "Float To Int"
