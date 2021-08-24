import bpy
from bpy.types import Node
from ..utils import send_value


class RenderEngineNode(Node):
    """Render Engine"""
    bl_idname = 'RenderEngineNodeType'
    bl_label = 'Render Engine'

    render_engine: bpy.props.EnumProperty(
        items=(('CYCLES', 'Cycles', 'Engine to use: Cycles'),
               ('BLENDER_EEVEE', 'Eevee', 'Engine to use: Eevee'),
               ('BLENDER_WORKBENCH', 'Workbench', 'Engine to use: Workbench')),
        name='Engine')

    def init(self, context):
        self.outputs.new('NodeSocketFloat', 'is_active')

    def update(self):
        scene = bpy.context.scene
        for output in self.outputs:
            if output.name == 'is_active':
                if self.render_engine == scene.render.engine:
                    send_value(self.outputs, 1)
                else:
                    send_value(self.outputs, 0)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'render_engine')

    def draw_label(self):
        return 'Render Engine'
