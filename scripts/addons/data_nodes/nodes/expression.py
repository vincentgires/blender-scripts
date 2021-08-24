import bpy
from bpy.types import Node
import string
from ..utils import send_value

operation_items = (
    ('expression', 'Expression', ''),
    ('add', 'Add', ''),
    ('subtract', 'Subtract', ''),
    ('multiply', 'Multiply', ''),
    ('divide', 'Divide', ''))


class Expression(Node):
    """Expression node"""
    bl_idname = 'ExpressionNodeType'
    bl_label = 'Expression'

    def update_props(self, context):
        self.update()

    operation_enum: bpy.props.EnumProperty(
        name='', items=operation_items, update=update_props)
    expr_prop: bpy.props.StringProperty(
        name='', update=update_props)

    def init(self, context):
        self.inputs.new('NodeSocketFloat', 'A')
        self.inputs.new('NodeSocketFloat', 'B')
        self.outputs.new('NodeSocketFloat', 'Value')

    def update(self):
        # Create variable for all inputs
        for input in self.inputs:
            exec(input.name + '=' + str(input.default_value))

        if self.operation_enum == 'expression':
            if self.expr_prop:
                output_value = eval(self.expr_prop)
            else:
                output_value = None
        else:
            try:
                output_value = self.inputs[0].default_value
            except:
                output_value = None
            if self.operation_enum == 'add':
                for input in self.inputs[1:]:
                    output_value = output_value + input.default_value
            if self.operation_enum == 'subtract':
                for input in self.inputs[1:]:
                    output_value = output_value - input.default_value
            if self.operation_enum == 'multiply':
                for input in self.inputs[1:]:
                    output_value = output_value * input.default_value
            if self.operation_enum == 'divide':
                for input in self.inputs[1:]:
                    output_value = output_value / input.default_value

        if isinstance(output_value, float) or isinstance(output_value, int):
            # Send data value to connected nodes
            send_value(self.outputs, output_value)

    def draw_buttons(self, context, layout):
        """Additional buttons displayed on the node"""

        layout.prop(self, 'operation_enum')
        if self.operation_enum == 'expression':
            layout.prop(self, 'expr_prop')
        row = layout.row(align=True)
        row.operator('add_input_socket_to_expression_node.btn', icon='ADD')
        row.operator('remove_input_sockets.btn', text='', icon='X')

    def draw_label(self):
        return 'Expression'


class ExpressionNodeAddInputSocket(bpy.types.Operator):
    bl_idname = 'add_input_socket_to_expression_node.btn'
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
