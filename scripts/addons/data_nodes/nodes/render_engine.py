import bpy
from bpy.types import Node
from ..utils import set_sockets


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
        self.outputs.new('NodeSocketFloat', 'Active')

    def update(self):
        scene = bpy.context.scene
        for output in self.outputs:
            if self.render_engine == scene.render.engine:
                set_sockets(output, 1)
            else:
                set_sockets(output, 0)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'render_engine')

    def draw_label(self):
        return 'Render Engine'
