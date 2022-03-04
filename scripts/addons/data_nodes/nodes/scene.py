import bpy
from bpy.types import Node
from ..utils import set_sockets


class SceneNode(Node):
    """Scene"""
    bl_idname = 'SceneNodeType'
    bl_label = 'Scene'

    def scene_enum(self, context):
        data = bpy.data
        items = [(scene.name, scene.name, '') for scene in data.scenes]
        return items

    scene: bpy.props.EnumProperty(
        items=scene_enum, name='Scene')

    def init(self, context):
        self.outputs.new('NodeSocketFloat', 'Active')

    def update(self):
        context = bpy.context
        for output in self.outputs:
            if self.scene == context.scene.name:
                set_sockets(output, 1)
            else:
                set_sockets(output, 0)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'scene')

    def draw_label(self):
        return 'Scene'
