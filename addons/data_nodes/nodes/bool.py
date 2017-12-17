import bpy
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.utils import send_value


class Bool(Node):
    '''Bool node'''
    bl_idname = 'BoolNodeType'
    bl_label = 'Bool'
    
    def update_props(self, context):
        self.update()
    
    bool_prop = bpy.props.BoolProperty(
        name="Bool",
        default=True,
        update=update_props)
    
    def init(self, context):
        self.outputs.new('NodeSocketBool', "Bool")
    
    def update(self):
        # send data value to connected nodes
        send_value(self.outputs, self.bool_prop)
                    
    def draw_buttons(self, context, layout):
        layout.prop(self, "bool_prop")
    
    def draw_label(self):
        return "Bool"
