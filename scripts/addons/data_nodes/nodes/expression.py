import bpy
from bpy.types import Node
import string
from ..utils import send_value
import numpy

operation_items = (
    ('EXPRESSION', 'Expression', ''),
    ('ADD', 'Add', ''),
    ('SUBTRACT', 'Subtract', ''),
    ('MULTIPLY', 'Multiply', ''),
    ('DIVIDE', 'Divide', ''))


class Expression(Node):
    """Expression node"""
    bl_idname = 'ExpressionNodeType'
    bl_label = 'Expression'

    def update_props(self, context):
        self.update()

    operation: bpy.props.EnumProperty(
        name='Operation', items=operation_items, update=update_props)
    expression: bpy.props.StringProperty(
        name='Expression', update=update_props)

    def init(self, context):
        self.inputs.new('NodeSocketFloat', 'A')
        self.inputs.new('NodeSocketFloat', 'B')
        self.outputs.new('NodeSocketFloat', 'Value')

    def update(self):
        if not self.inputs:
            return
        values = {i.name: i.default_value for i in self.inputs}
        if self.operation == 'EXPRESSION':
            if not self.expression:
                return
            expr = list(self.expression)
            for index, i in enumerate(expr):
                v = values.get(i)
                if v is not None:
                    expr[index] = str(v)
            send_value(self.outputs, eval(''.join(expr)))
        elif self.operation == 'ADD':
            send_value(self.outputs, numpy.sum(list(values.values())))
        elif self.operation == 'SUBTRACT':
            vv = list(values.values())
            v = [vv[0]] + [v * -1 for v in vv[1:]]
            send_value(self.outputs, numpy.sum(v))
        elif self.operation == 'MULTIPLY':
            send_value(self.outputs, numpy.prod(list(values.values())))
        elif self.operation == 'DIVIDE':
            vv = list(values.values())
            v = [vv[0]] + [1 / v for v in vv[1:]]
            send_value(self.outputs, numpy.prod(v))

    def draw_buttons(self, context, layout):
        layout.prop(self, 'operation')
        if self.operation == 'EXPRESSION':
            layout.prop(self, 'expression')
        row = layout.row(align=True)
        row.operator('scene.add_input_socket_to_expression_node', icon='ADD')
        remove_sockets = row.operator(
            'scene.remove_sockets', text='', icon='X')
        remove_sockets.socket_type = 'INPUT'

    def draw_label(self):
        return 'Expression'


class ExpressionNodeAddInputSocket(bpy.types.Operator):
    bl_idname = 'scene.add_input_socket_to_expression_node'
    bl_label = 'Add input'
    bl_description = 'Add input socket to the node'

    @classmethod
    def poll(cls, context):
        tree_type = context.space_data.tree_type
        node_tree = ['ShaderNodeTree', 'CompositorNodeTree', 'DataNodeTree']
        return tree_type in node_tree

    def execute(self, context):
        node = context.node
        selected_object = context.object
        alphabet = list(string.ascii_uppercase)
        node.inputs.new('NodeSocketFloat', alphabet[len(node.inputs)])
        return {'FINISHED'}
