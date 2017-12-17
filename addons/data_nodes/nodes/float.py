import bpy
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.utils import send_value


class Float(Node):
    '''Float node'''
    bl_idname = 'FloatNodeType'
    bl_label = 'Float'
    
    def update_props(self, context):
        self.update()
    
    float_prop = bpy.props.FloatProperty(
        name='Float', default=1.0, update=update_props)
    
    def init(self, context):
        self.outputs.new('NodeSocketFloat', "Float")
    
    def update(self):
        # send data value to connected nodes
        send_value(self.outputs, self.float_prop)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "float_prop")
    
    def draw_label(self):
        return "Float"
