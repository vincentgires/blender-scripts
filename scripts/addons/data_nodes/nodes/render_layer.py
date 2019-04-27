import bpy
from bpy.app.handlers import persistent
from bpy.types import NodeTree, Node, NodeSocket
from data_nodes.utils import send_value


class RenderLayersNode(Node):
    '''Render Layers'''
    bl_idname = 'RenderLayersNodeType'
    bl_label = 'Render Layers'
    
    def renderlayers_enum(self,context):
        scene = context.scene
        items = [(layer.name, layer.name, '') for layer in scene.render.layers]
        return items
    
    render_layers = bpy.props.EnumProperty(
        items=renderlayers_enum, name = 'Layer')
    
    def init(self, context):
        self.outputs.new('NodeSocketFloat', 'is_active')
     
    def update(self):
        scene = bpy.context.scene
        active_layer = scene.render.layers.active.name
        for output in self.outputs:
            if output.name == 'is_active':
                if self.render_layers == active_layer:
                    send_value(self.outputs, 1)
                else:
                    send_value(self.outputs, 0)
    
    def draw_buttons(self, context, layout):
        layout.prop(self, "render_layers")

    def draw_label(self):
        return "Render Layers"


