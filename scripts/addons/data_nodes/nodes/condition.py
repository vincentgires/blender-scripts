import bpy
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.utils import send_value

operation_items = (
    ('==', '==', ''),
    ('!=', '!=', ''),
    ('>', '>', ''),
    ('>=', '>=', ''),
    ('<', '<', ''),
    ('<=', '<=', ''),
    ('and', 'and', ''),
    ('or', 'or', ''),
    ('not', 'not', '')
    )


class Condition(Node):
    '''Expression node'''
    bl_idname = 'ConditionNodeType'
    bl_label = 'Condition'
    
    def update_props(self, context):
        self.update()
    
    operation_enum = bpy.props.EnumProperty(
        name='',
        items=operation_items,
        update=update_props)
    
    def init(self, context):
        self.inputs.new('NodeSocketFloat', "A")
        self.inputs.new('NodeSocketFloat', "B")
        self.outputs.new('NodeSocketFloat', "Value")
    
    def update(self):
        
        if len(self.inputs) >= 2:
            
            A = self.inputs["A"].default_value
            B = self.inputs["B"].default_value
            
            if self.operation_enum == "==":
                send_value(self.outputs, A == B)
                
            elif self.operation_enum == "!=":
                send_value(self.outputs, A != B)
                
            elif self.operation_enum == ">":
                send_value(self.outputs, A > B)
                
            elif self.operation_enum == ">=":
                send_value(self.outputs, A >= B)
                
            elif self.operation_enum == "<":
                send_value(self.outputs, A < B)
                
            elif self.operation_enum == "<=":
                send_value(self.outputs, A <= B)
                
            elif self.operation_enum == "and":
                send_value(self.outputs, A and B)
                
            elif self.operation_enum == "or":
                send_value(self.outputs, A or B)
                
            elif self.operation_enum == "not":
                send_value(self.outputs, not A)
                
            else:
                send_value(self.outputs, False)
            
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "operation_enum")
    
    def draw_label(self):
        return "Condition"
