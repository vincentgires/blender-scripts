import bpy
from bpy.types import Node
from ..utils import send_value


class ViewLayerNode(Node):
    """View Layer"""
    bl_idname = 'ViewLayerNodeType'
    bl_label = 'View Layer'

    def view_layer_enum(self, context):
        scene = context.scene
        items = [(layer.name, layer.name, '') for layer in scene.view_layers]
        return items

    view_layer: bpy.props.EnumProperty(
        items=view_layer_enum, name='Layer')

    def init(self, context):
        self.outputs.new('NodeSocketFloat', 'is_active')

    def update(self):
        context = bpy.context
        for output in self.outputs:
            if output.name == 'is_active':
                if self.view_layer == context.view_layer.name:
                    send_value(self.outputs, 1)
                else:
                    send_value(self.outputs, 0)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'view_layer')

    def draw_label(self):
        return 'View Layer'
