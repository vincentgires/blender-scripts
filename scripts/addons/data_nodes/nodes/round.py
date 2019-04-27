import bpy
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.utils import send_value


class FloatToString(Node):
    '''Float To String node'''
    bl_idname = 'RoundNodeType'
    bl_label = 'Round'
    
    def init(self, context):
        self.inputs.new('NodeSocketFloat', "Float")
        self.outputs.new('NodeSocketFloat', "Float")
        self.outputs.new('NodeSocketInt', "Int")
    
    def update(self):
        input_value = self.inputs["Float"].default_value
        input_value = round(input_value)
        
        # send data value to connected nodes
        send_value(self.outputs, input_value)
    
    def draw_label(self):
        return "Round"
