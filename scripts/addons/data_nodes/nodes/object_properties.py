import bpy
from bpy.types import Node
from ..utils import set_sockets


class ObjectPropertiesNode(Node):
    """Object Properties node"""
    bl_idname = 'ObjectPropertiesNodeType'
    bl_label = 'Object Properties'

    item: bpy.props.StringProperty(
        name='Object')
    invert_matrix: bpy.props.BoolProperty(
        name='Invert matrix',
        default=False)

    def get_object(self):
        if not self.item:
            return
        ob = bpy.context.scene.objects[self.item]
        return ob

    def get_location(self):
        ob = self.get_object()
        if ob is not None:
            return ob.location

    def get_rotation(self):
        ob = self.get_object()
        if ob is not None:
            return ob.rotation_euler

    def get_scale(self):
        ob = self.get_object()
        if ob is not None:
            return ob.scale

    def get_matrix(self, row=None):
        ob = self.get_object()
        if ob is None:
            return
        matrix = ob.matrix_world.to_3x3()
        if self.invert_matrix:
            matrix = matrix.inverted()
        if row is None:
            return matrix
        else:
            return matrix[row]

    def init(self, context):
        for socket_name in (
                'Location', 'Rotation', 'Scale',
                'Matrix Row1', 'Matrix Row2', 'Matrix Row3'):
            self.outputs.new('NodeSocketVector', socket_name)

    def update(self):
        if self.get_object() is None:
            return
        for output in self.outputs:
            if output.name == 'Location':
                set_sockets(output, self.get_location())
            elif output.name == 'Rotation':
                set_sockets(output, self.get_rotation())
            elif output.name == 'Scale':
                set_sockets(output, self.get_scale())
            elif output.name == 'Matrix Row1':
                set_sockets(output, self.get_matrix(row=0))
            elif output.name == 'Matrix Row2':
                set_sockets(output, self.get_matrix(row=1))
            elif output.name == 'Matrix Row3':
                set_sockets(output, self.get_matrix(row=2))

    def draw_buttons(self, context, layout):
        row = layout.row(align=True)
        row.prop_search(
            self, 'item', bpy.data, 'objects',
            icon='OBJECT_DATA', text='')
        row.operator(
            'scene.get_object_to_data_node', text='', icon='EYEDROPPER')
        layout.prop(self, 'invert_matrix')

    def draw_buttons_ext(self, context, layout):
        row = layout.row(align=True)
        row.prop_search(self, 'item', bpy.data, 'objects', icon='OBJECT_DATA')
        row.operator(
            'scene.get_object_to_data_node', text='', icon='EYEDROPPER')
        box = layout.box()
        box.prop(self, 'invert_matrix')
        if self.get_object() is not None:
            row = box.row()
            row.label(text=str(self.get_matrix(row=0)[0]))
            row.label(text=str(self.get_matrix(row=0)[1]))
            row.label(text=str(self.get_matrix(row=0)[2]))
            row = box.row()
            row.label(text=str(self.get_matrix(row=1)[0]))
            row.label(text=str(self.get_matrix(row=1)[1]))
            row.label(text=str(self.get_matrix(row=1)[2]))
            row = box.row()
            row.label(text=str(self.get_matrix(row=2)[0]))
            row.label(text=str(self.get_matrix(row=2)[1]))
            row.label(text=str(self.get_matrix(row=2)[2]))

    def draw_label(self):
        return 'Object Properties'
