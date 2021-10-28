import bpy
from bpy.types import Node
from ..utils import send_value


class NoteNode(Node):
    """Note node"""
    bl_idname = 'NoteNodeType'
    bl_label = 'Note'

    def update_attribute(self, context):
        self.update()

    note: bpy.props.StringProperty(
        name='Note', update=update_attribute)

    def init(self, context):
        self.outputs.new('NodeSocketString', 'String')

    def update(self):
        send_value(self.outputs, self.note)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'note', text='')

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, 'note')

    def draw_label(self):
        return 'Note'
