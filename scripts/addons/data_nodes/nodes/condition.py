import bpy
from bpy.types import Node
from ..utils import send_value

operation_items = (
    ('==', '==', ''),
    ('!=', '!=', ''),
    ('>', '>', ''),
    ('>=', '>=', ''),
    ('<', '<', ''),
    ('<=', '<=', ''),
    ('AND', 'and', ''),
    ('OR', 'or', ''),
    ('NOT', 'not', ''))


class Condition(Node):
    """Expression node"""
    bl_idname = 'ConditionNodeType'
    bl_label = 'Condition'

    def update_props(self, context):
        self.update()

    operation: bpy.props.EnumProperty(
        name='Operation',
        items=operation_items,
        update=update_props)

    def init(self, context):
        self.inputs.new('NodeSocketFloat', 'A')
        self.inputs.new('NodeSocketFloat', 'B')
        self.outputs.new('NodeSocketFloat', 'Value')

    def update(self):
        if len(self.inputs) >= 2:
            a = self.inputs['A'].default_value
            b = self.inputs['B'].default_value
            if self.operation == '==':
                send_value(self.outputs, a == b)
            elif self.operation == '!=':
                send_value(self.outputs, a != b)
            elif self.operation == '>':
                send_value(self.outputs, a > b)
            elif self.operation == '>=':
                send_value(self.outputs, a >= b)
            elif self.operation == '<':
                send_value(self.outputs, a < b)
            elif self.operation == '<=':
                send_value(self.outputs, a <= b)
            elif self.operation == 'AND':
                send_value(self.outputs, a and b)
            elif self.operation == 'OR':
                send_value(self.outputs, a or b)
            elif self.operation == 'NOT':
                send_value(self.outputs, not a)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operation')

    def draw_label(self):
        return 'Condition'
